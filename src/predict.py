import os
import json
import logging
import torch
import torchvision.transforms as transforms
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_prediction_model(model_path, model_name="mobilenet_v3_large", num_classes=15, device="cpu"):
    """
    Loads a saved PyTorch model with exception handling.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Missing model: No file found at {model_path}")
        
    try:
        from src.model import get_plant_model
        # Construct model structure
        model = get_plant_model(model_name=model_name, num_classes=num_classes, pretrained=False)
        
        # Get classifier output features before prediction
        if model_name == "mobilenet_v3_large":
            out_features = model.classifier[3].out_features
        else:
            out_features = model.classifier[1].out_features
        logging.info(f"[DEBUG] Model Classifier Output Dimension before loading weights: {out_features}")
        
        # Load weights
        state_dict = torch.load(model_path, map_location=device)
        
        # Verify keys manually
        model_keys = set(model.state_dict().keys())
        ckpt_keys = set(state_dict.keys())
        missing_keys = model_keys - ckpt_keys
        unexpected_keys = ckpt_keys - model_keys
        
        if missing_keys:
            logging.warning(f"[WARNING] Missing keys in state_dict: {missing_keys}")
        if unexpected_keys:
            logging.warning(f"[WARNING] Unexpected keys in state_dict: {unexpected_keys}")
            
        # Do NOT use strict=False
        model.load_state_dict(state_dict, strict=True)
        model = model.to(device)
        model.eval()
        
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        logging.info(f"[DEBUG] Loaded model architecture: {model_name}")
        logging.info(f"[DEBUG] Total Parameters: {total_params:,} | Trainable Parameters: {trainable_params:,}")
        logging.info(f"[DEBUG] Device: {device}")
        
        logging.info(f"Successfully loaded model from {model_path} onto {device} (strict loading succeeded).")
        return model
    except Exception as e:
        raise RuntimeError(f"Error loading model state dictionary: {e}") from e

def load_class_indices(json_path):
    """
    Loads class to index mapping and returns index to class name dictionary.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Missing class indices config: No file found at {json_path}")
        
    try:
        with open(json_path, 'r') as f:
            class_to_idx = json.load(f)
        idx_to_class = {v: k for k, v in class_to_idx.items()}
        return idx_to_class
    except Exception as e:
        raise ValueError(f"Could not parse class indices JSON: {e}") from e

def predict_single_image(model, image_path, idx_to_class, img_size=224, device="cpu", show_image=True):
    """
    Performs inference on a single image and prints prediction details.
    """
    # 1. Exception handling for missing/corrupted image
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Invalid image: File does not exist at {image_path}")
        
    try:
        # Load image using PIL to check for corruption
        with open(image_path, 'rb') as f:
            img = Image.open(f)
            img.verify() # Verify it is a valid image
            
        # Re-open after verify() since verify() closes the file pointer
        with open(image_path, 'rb') as f:
            img = Image.open(f)
            img = img.convert('RGB')
    except Exception as e:
        raise ValueError(f"Corrupted or invalid image: Failed to open and parse {image_path}. Error: {e}") from e

    # 2. Setup transforms (must align exactly with validation transforms: Resize, CenterCrop, Normalize)
    transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.CenterCrop(img_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # 3. Preprocess and run inference
    input_tensor = transform(img).unsqueeze(0).to(device)
    
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        
    # Print raw logits and softmax probabilities for debugging
    raw_logits_np = outputs[0].cpu().numpy()
    probabilities_np = probabilities.cpu().numpy()
    prob_sum = probabilities.sum().item()
    
    print("\n" + "="*50)
    print("DEBUGGING PROBABILITIES AND LOGITS")
    print("="*50)
    print(f"Raw Logits: {raw_logits_np}")
    print(f"Softmax Probabilities: {probabilities_np}")
    print(f"Sum of Softmax Probabilities: {prob_sum:.6f} (Verification: Should be 1.0)")
    print("="*50 + "\n")
        
    # 4. Get Top 3 Predictions
    topk_probs, topk_indices = torch.topk(probabilities, k=min(3, len(idx_to_class)))
    
    topk_probs = topk_probs.cpu().numpy()
    topk_indices = topk_indices.cpu().numpy()
    
    predicted_class = idx_to_class[topk_indices[0]]
    predicted_confidence = topk_probs[0] * 100
    
    print("\n" + "="*50)
    print("PREDICTION RESULT")
    print("="*50)
    print(f"Predicted Disease: {predicted_class}")
    print(f"Confidence Percentage: {predicted_confidence:.2f}%")
    print("\nTop 3 Predictions:")
    for idx, (prob, class_idx) in enumerate(zip(topk_probs, topk_indices)):
        print(f"  {idx + 1}. {idx_to_class[class_idx]}: {prob * 100:.2f}%")
    print("="*50 + "\n")
    
    # 5. Display/Save the input image with prediction title
    if show_image:
        plt.figure(figsize=(6, 6))
        plt.imshow(img)
        plt.title(f"Predicted: {predicted_class}\nConfidence: {predicted_confidence:.2f}%", fontsize=12, color='green')
        plt.axis('off')
        out_img_path = "prediction_output.png"
        plt.savefig(out_img_path, bbox_inches='tight')
        plt.close()
        logging.info(f"Saved prediction visualization to {out_img_path}")
        
    return {
        'prediction': predicted_class,
        'confidence': predicted_confidence,
        'top_3': [(idx_to_class[class_idx], float(prob)) for prob, class_idx in zip(topk_probs, topk_indices)]
    }
