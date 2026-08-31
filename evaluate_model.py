import os
import argparse
import logging
import torch
from src.dataset import get_dataloaders
from src.predict import load_prediction_model
from src.eval import evaluate_model_on_test

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Plant Disease Detection Evaluation Script")
    parser.add_argument("--model-path", type=str, default="best_model.pth", help="Path to saved model (.pth)")
    parser.add_argument("--class-indices", type=str, default="class_indices.json", help="Path to class indices mapping JSON")
    parser.add_argument("--dataset-dir", type=str, default="PlantVillage", help="Path to PlantVillage dataset folder")
    parser.add_argument("--model-name", type=str, default="mobilenet_v3_large", choices=["mobilenet_v3_large", "mobilenet_v2"], help="Model backbone used")
    parser.add_argument("--batch-size", type=int, default=32, help="Mini-batch size")
    
    args = parser.parse_args()
    
    # 1. Exception Handling: check dataset & files
    if not os.path.exists(args.dataset_dir):
        logging.error(f"Missing dataset: Directory not found at {args.dataset_dir}")
        return
    if not os.path.exists(args.class_indices):
        logging.error(f"Missing config: Class indices not found at {args.class_indices}")
        return
        
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"Using device: {device}")
    
    # 2. Get dataloaders
    try:
        _, _, test_loader, class_to_idx = get_dataloaders(
            dataset_dir=args.dataset_dir,
            batch_size=args.batch_size
        )
    except Exception as e:
        logging.error(f"Error loading dataset: {e}")
        return
        
    num_classes = len(class_to_idx)
    
    # 3. Load model
    try:
        model = load_prediction_model(
            model_path=args.model_path,
            model_name=args.model_name,
            num_classes=num_classes,
            device=device.type
        )
    except Exception as e:
        logging.error(f"Error initializing prediction model: {e}")
        return
        
    # 4. Evaluate
    try:
        evaluate_model_on_test(
            model=model,
            test_loader=test_loader,
            class_to_idx=class_to_idx,
            device=device.type,
            output_dir="."
        )
    except Exception as e:
        logging.error(f"Failed to execute evaluation: {e}")

if __name__ == "__main__":
    main()
