import os
import argparse
import logging
import torch
from src.predict import load_prediction_model, load_class_indices, predict_single_image

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Plant Disease Detection Single Image Inference Script")
    parser.add_argument("--image-path", type=str, required=True, help="Path to input image file")
    parser.add_argument("--model-path", type=str, default="best_model.pth", help="Path to saved model weights (.pth)")
    parser.add_argument("--class-indices", type=str, default="class_indices.json", help="Path to class mapping indices JSON")
    parser.add_argument("--model-name", type=str, default="mobilenet_v3_large", choices=["mobilenet_v3_large", "mobilenet_v2"], help="Model backbone architecture")
    
    args = parser.parse_args()
    
    # 1. Device check and fallback
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"Configured prediction device: {device}")
    
    # 2. Load mapping
    try:
        idx_to_class = load_class_indices(args.class_indices)
    except Exception as e:
        logging.error(f"Error loading configurations: {e}")
        return
        
    num_classes = len(idx_to_class)
    
    # 3. Load model
    try:
        model = load_prediction_model(
            model_path=args.model_path,
            model_name=args.model_name,
            num_classes=num_classes,
            device=device.type
        )
    except Exception as e:
        logging.error(f"Error during model startup: {e}")
        return
        
    # 4. Run inference
    try:
        predict_single_image(
            model=model,
            image_path=args.image_path,
            idx_to_class=idx_to_class,
            device=device.type,
            show_image=True
        )
    except Exception as e:
        logging.error(f"Prediction failed: {e}")

if __name__ == "__main__":
    main()
