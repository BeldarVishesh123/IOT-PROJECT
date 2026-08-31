import os
import json
import logging
import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def evaluate_model_on_test(model, test_loader, class_to_idx, device="cpu", output_dir="."):
    """
    Evaluates the model on the test dataloader and generates metrics, report, and confusion matrix.
    """
    model.eval()
    all_preds = []
    all_labels = []
    
    idx_to_class = {v: k for k, v in class_to_idx.items()}
    class_names = [idx_to_class[i] for i in range(len(class_to_idx))]
    
    logging.info(f"Evaluating model on test dataset using device: {device}...")
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())
            
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    
    # Calculate Metrics
    accuracy = accuracy_score(all_labels, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_preds, average='weighted', zero_division=0)
    
    report = classification_report(all_labels, all_preds, target_names=class_names, labels=list(range(len(class_names))), zero_division=0)
    cm = confusion_matrix(all_labels, all_preds, labels=list(range(len(class_names))))
    
    # Print Metrics to console
    print("\n" + "="*50)
    print("TEST EVALUATION METRICS")
    print("="*50)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")
    print(f"Precision (Weighted): {precision:.4f}")
    print(f"Recall (Weighted): {recall:.4f}")
    print(f"F1 Score (Weighted): {f1:.4f}")
    print("\nClassification Report:")
    print(report)
    print("="*50 + "\n")
    
    # Plot and save Confusion Matrix
    plt.figure(figsize=(12, 10))
    # Using simple matrix display or sns (seaborn) if installed, else matplotlib matshow
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=90)
    plt.yticks(tick_marks, class_names)
    
    # Add values to the cells
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                     ha="center", va="center",
                     color="white" if cm[i, j] > thresh else "black")
            
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
    cm_path = os.path.join(output_dir, 'confusion_matrix.png')
    plt.savefig(cm_path, bbox_inches='tight')
    plt.close()
    logging.info(f"Confusion Matrix saved to: {cm_path}")
    
    metrics = {
        'test_accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'classification_report': report
    }
    
    return metrics

def plot_training_history(history_json_path, output_dir="."):
    """
    Reads training history from JSON file and generates Accuracy and Loss plots.
    """
    with open(history_json_path, 'r') as f:
        history = json.load(f)
        
    epochs = range(1, len(history['train_loss']) + 1)
    
    # 1. Accuracy Curve
    plt.figure(figsize=(8, 6))
    plt.plot(epochs, [a * 100 for a in history['train_acc']], 'b-o', label='Training Accuracy')
    plt.plot(epochs, [a * 100 for a in history['val_acc']], 'r-s', label='Validation Accuracy')
    plt.title('Accuracy vs Epoch')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.grid(True)
    plt.legend()
    acc_plot_path = os.path.join(output_dir, 'accuracy_vs_epoch.png')
    plt.savefig(acc_plot_path)
    plt.close()
    logging.info(f"Accuracy graph saved to: {acc_plot_path}")
    
    # 2. Loss Curve
    plt.figure(figsize=(8, 6))
    plt.plot(epochs, history['train_loss'], 'b-o', label='Training Loss')
    plt.plot(epochs, history['val_loss'], 'r-s', label='Validation Loss')
    plt.title('Loss vs Epoch')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True)
    plt.legend()
    loss_plot_path = os.path.join(output_dir, 'loss_vs_epoch.png')
    plt.savefig(loss_plot_path)
    plt.close()
    logging.info(f"Loss graph saved to: {loss_plot_path}")
