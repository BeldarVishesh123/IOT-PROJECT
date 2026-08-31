import time
import json
import logging
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau, CosineAnnealingLR
import copy

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EarlyStopping:
    """
    Early stops the training if validation loss doesn't improve after a given patience.
    """
    def __init__(self, patience=5, verbose=False, delta=0):
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_loss = None
        self.early_stop = False
        self.delta = delta

    def __call__(self, val_loss):
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss > self.best_loss - self.delta:
            self.counter += 1
            if self.verbose:
                logging.info(f"EarlyStopping counter: {self.counter} out of {self.patience}")
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_loss = val_loss
            self.counter = 0

def format_time(seconds):
    """Formats seconds to H:M:S string."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}s"
    else:
        return f"{s}s"

def train_model(model, train_loader, val_loader, num_epochs=10, initial_lr=1e-3, 
                patience=5, device="cpu", fine_tune_after_epoch=None, fine_tune_lr=1e-5,
                best_model_path="best_model.pth", final_model_path="final_model.pth"):
    """
    Runs the model training pipeline.
    """
    # 1. Print detected dataset details
    # Attempt to extract classes from loaders if possible, or print from model
    logging.info(f"[DEBUG] Starting training: Device is {device}")
    
    # Get classifier output features
    if hasattr(model, 'classifier') and isinstance(model.classifier, nn.Sequential):
        if len(model.classifier) > 3 and hasattr(model.classifier[3], 'out_features'):
            out_features = model.classifier[3].out_features
        elif len(model.classifier) > 1 and hasattr(model.classifier[1], 'out_features'):
            out_features = model.classifier[1].out_features
        else:
            out_features = "unknown"
    else:
        out_features = "unknown"
        
    logging.info(f"[DEBUG] Classifier Output Dimension before training starts: {out_features}")
    
    model = model.to(device)
    
    # Calculate class weights for training set to handle class imbalance
    if hasattr(train_loader.dataset, 'labels'):
        train_labels = train_loader.dataset.labels
        from collections import Counter
        class_counts = Counter(train_labels)
        total_samples = len(train_labels)
        num_classes = len(class_counts)
        
        # Calculate weights: total_samples / (num_classes * count)
        weights = [total_samples / (num_classes * class_counts[i]) for i in range(num_classes)]
        class_weights = torch.FloatTensor(weights).to(device)
        logging.info(f"[DEBUG] Calculated class weights for loss function: {weights}")
        criterion = nn.CrossEntropyLoss(weight=class_weights)
    else:
        logging.warning("[WARNING] Dataset does not have labels attribute. Using unweighted CrossEntropyLoss.")
        criterion = nn.CrossEntropyLoss()
    
    # Optimizer (AdamW)
    optimizer = AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=initial_lr, weight_decay=1e-2)
    
    # LR Scheduler
    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2)
    
    early_stopping = EarlyStopping(patience=patience, verbose=True)
    
    best_model_wts = copy.deepcopy(model.state_dict())
    best_val_loss = float('inf')
    
    history = {
        'train_loss': [],
        'val_loss': [],
        'train_acc': [],
        'val_acc': [],
        'learning_rates': []
    }
    
    start_time = time.time()
    
    logging.info(f"Starting training on device: {device}")
    
    for epoch in range(1, num_epochs + 1):
        epoch_start = time.time()
        
        # Check if fine-tuning needs to trigger
        if fine_tune_after_epoch is not None and epoch == fine_tune_after_epoch + 1:
            logging.info("Fine-tuning trigger: Unfreezing backbone layers...")
            from src.model import unfreeze_model_backbone
            unfreeze_model_backbone(model)
            # Recreate optimizer with all parameters
            optimizer = AdamW(model.parameters(), lr=fine_tune_lr, weight_decay=1e-2)
            # Recreate scheduler
            scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2)
            
        # Training Phase
        model.train()
        running_loss = 0.0
        running_corrects = 0
        total_train_samples = 0
        
        batch_times = []
        for batch_idx, (inputs, labels) in enumerate(train_loader):
            batch_start = time.time()
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            
            # Print gradient norms for debugging (verifying updates occur)
            if batch_idx == 0:
                grad_norms = [p.grad.norm().item() for p in model.parameters() if p.grad is not None]
                if grad_norms:
                    avg_grad = sum(grad_norms) / len(grad_norms)
                    logging.info(f"[DEBUG] Epoch {epoch} Batch 1 | Avg Gradient Norm: {avg_grad:.6f} (Gradients are active and updating)")
                else:
                    logging.warning(f"[WARNING] Epoch {epoch} Batch 1 | No active gradients detected (all frozen?)")
                    
            optimizer.step()
            
            # Statistics
            running_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            running_corrects += torch.sum(preds == labels.data).item()
            total_train_samples += inputs.size(0)
            
            batch_times.append(time.time() - batch_start)
            
            # Print intermediate progress for long epochs
            if (batch_idx + 1) % 100 == 0 or batch_idx == len(train_loader) - 1:
                avg_batch_time = sum(batch_times) / len(batch_times)
                batches_left = len(train_loader) - (batch_idx + 1)
                est_batch_time_left = batches_left * avg_batch_time
                # Also estimate remaining epochs
                epochs_left = num_epochs - epoch
                est_epoch_time = len(train_loader) * avg_batch_time
                est_total_remaining = est_batch_time_left + (epochs_left * est_epoch_time)
                
                logging.info(
                    f"Epoch {epoch}/{num_epochs} | Batch {batch_idx + 1}/{len(train_loader)} | "
                    f"Batch ETA: {format_time(est_batch_time_left)} | Overall ETA: {format_time(est_total_remaining)}"
                )
                
        train_loss = running_loss / total_train_samples
        train_acc = running_corrects / total_train_samples
        
        # Validation Phase
        model.eval()
        val_loss = 0.0
        val_corrects = 0
        total_val_samples = 0
        
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs = inputs.to(device)
                labels = labels.to(device)
                
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item() * inputs.size(0)
                _, preds = torch.max(outputs, 1)
                val_corrects += torch.sum(preds == labels.data).item()
                total_val_samples += inputs.size(0)
                
        val_loss = val_loss / total_val_samples
        val_acc = val_corrects / total_val_samples
        
        current_lr = optimizer.param_groups[0]['lr']
        
        # Record history
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        history['train_acc'].append(train_acc)
        history['val_acc'].append(val_acc)
        history['learning_rates'].append(current_lr)
        
        # Step the scheduler
        scheduler.step(val_loss)
        
        # Time tracking
        epoch_end = time.time()
        epoch_duration = epoch_end - epoch_start
        epochs_left = num_epochs - epoch
        estimated_remaining_time = epochs_left * epoch_duration
        
        # Visual output formatting according to user request
        print("\n" + "="*50)
        print(f"Epoch: {epoch}/{num_epochs}")
        print(f"Training Loss: {train_loss:.4f}")
        print(f"Validation Loss: {val_loss:.4f}")
        print(f"Training Accuracy: {train_acc * 100:.2f}%")
        print(f"Validation Accuracy: {val_acc * 100:.2f}%")
        print(f"Current Learning Rate: {current_lr:.6e}")
        print(f"Estimated Remaining Time: {format_time(estimated_remaining_time)}")
        print("="*50 + "\n")
        
        # Check if this is the best model so far
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_model_wts = copy.deepcopy(model.state_dict())
            logging.info(f"--> Found new best validation loss: {best_val_loss:.4f}. Saving weight copy to disk: {best_model_path}")
            torch.save(best_model_wts, best_model_path)
            
        # Check Early Stopping
        early_stopping(val_loss)
        if early_stopping.early_stop:
            logging.info("Early stopping triggered. Terminating training.")
            break
            
    # Load best weights before returning
    model.load_state_dict(best_model_wts)
    
    # Save final model weights
    logging.info(f"Saving final model weights to disk: {final_model_path}")
    torch.save(model.state_dict(), final_model_path)
    
    total_time = time.time() - start_time
    logging.info(f"Training complete in {format_time(total_time)}.")
    
    return model, history
