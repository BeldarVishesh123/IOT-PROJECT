import os
import argparse
import json
import logging
import torch
from src.dataset import get_dataloaders
from src.model import get_plant_model
from src.train import train_model
from src.eval import evaluate_model_on_test, plot_training_history

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Plant Disease Detection Training Pipeline")
    parser.add_argument("--dataset-dir", type=str, default="PlantVillage", help="Path to PlantVillage dataset folder")
    parser.add_argument("--model-name", type=str, default="mobilenet_v3_large", choices=["mobilenet_v3_large", "mobilenet_v2"], help="Backbone model selection")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Mini-batch size")
    parser.add_argument("--lr", type=float, default=1e-3, help="Initial learning rate")
    parser.add_argument("--patience", type=int, default=5, help="Patience for early stopping")
    parser.add_argument("--fine-tune-after", type=int, default=None, help="Epoch index after which backbone is unfrozen")
    parser.add_argument("--fine-tune-lr", type=float, default=1e-5, help="Learning rate for fine-tuning")
    
    args = parser.parse_args()
    
    # 1. Device check
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"Automatically configured device: {device}")
    
    # 2. Load dataloaders
    try:
        train_loader, val_loader, test_loader, class_to_idx = get_dataloaders(
            dataset_dir=args.dataset_dir,
            batch_size=args.batch_size
        )
    except Exception as e:
        logging.error(f"Failed to prepare dataloaders: {e}")
        return
        
    num_classes = len(class_to_idx)
    
    # Save class indices
    class_indices_path = "class_indices.json"
    with open(class_indices_path, "w") as f:
        json.dump(class_to_idx, f, indent=4)
    logging.info(f"Saved class mapping index file to {class_indices_path}")
    
    # 3. Model construction
    model = get_plant_model(
        model_name=args.model_name,
        num_classes=num_classes,
        pretrained=True,
        freeze_backbone=True
    )
    
    # 4. Execute training
    trained_model, history = train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        num_epochs=args.epochs,
        initial_lr=args.lr,
        patience=args.patience,
        device=device.type,
        fine_tune_after_epoch=args.fine_tune_after,
        fine_tune_lr=args.fine_tune_lr
    )
    
    # Save history
    history_path = "training_history.json"
    with open(history_path, "w") as f:
        json.dump(history, f, indent=4)
    logging.info(f"Saved training history stats to {history_path}")
    
    # Save final and best model (best model state is loaded inside train_model before returning)
    best_model_path = "best_model.pth"
    torch.save(trained_model.state_dict(), best_model_path)
    logging.info(f"Saved best performing model state dict to {best_model_path}")
    
    # Save final model (we save the state dict of the trained model as well)
    final_model_path = "final_model.pth"
    torch.save(trained_model.state_dict(), final_model_path)
    logging.info(f"Saved final model state dict to {final_model_path}")
    
    # 5. Generate plots
    plot_training_history(history_path, output_dir=".")
    
    # 6. Evaluate on Test set
    evaluate_model_on_test(
        model=trained_model,
        test_loader=test_loader,
        class_to_idx=class_to_idx,
        device=device.type,
        output_dir="."
    )
    
    # 7. Test on 20 unseen test images to verify class mapping
    logging.info("Testing model on 20 random unseen test images...")
    import random
    from src.predict import predict_single_image
    
    test_dataset = test_loader.dataset
    idx_to_class = {v: k for k, v in class_to_idx.items()}
    
    # Select 20 random indices
    test_size = len(test_dataset)
    random_indices = random.sample(range(test_size), min(20, test_size))
    
    successful_predictions = 0
    print("\n" + "="*80)
    print("VERIFICATION ON 20 UNSEEN TEST IMAGES")
    print("="*80)
    for count, idx in enumerate(random_indices):
        img_path = test_dataset.image_paths[idx]
        true_label_idx = test_dataset.labels[idx]
        true_class_name = idx_to_class[true_label_idx]
        
        # Call predict function without plotting to run fast
        pred_res = predict_single_image(
            model=trained_model,
            image_path=img_path,
            idx_to_class=idx_to_class,
            device=device.type,
            show_image=False
        )
        pred_class_name = pred_res['prediction']
        confidence = pred_res['confidence']
        
        status = "CORRECT" if pred_class_name == true_class_name else "INCORRECT"
        if pred_class_name == true_class_name:
            successful_predictions += 1
            
        print(f"[{count+1:2d}] True: {true_class_name:<45} | Pred: {pred_class_name:<45} | Conf: {confidence:6.2f}% | Status: {status}")
    print("="*80)
    print(f"Verification Success Rate: {successful_predictions}/20 ({successful_predictions/20*100:.1f}%)")
    print("="*80 + "\n")
    
    logging.info("Training and evaluation pipeline finished successfully!")

if __name__ == "__main__":
    main()
