import os
import sys
import logging
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.predict import load_prediction_model, load_class_indices

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GradCAM:
    """
    Grad-CAM (Gradient-weighted Class Activation Mapping) for MobileNetV3.
    Produces visual explanations for CNN decisions, highlighting lesion and pathogen regions.
    """
    def __init__(self, model, target_layer=None):
        self.model = model
        self.model.eval()
        self.gradients = None
        self.activations = None
        
        # Default target layer for MobileNetV3 is features[-1] (the final inverted residual block)
        if target_layer is None:
            self.target_layer = self.model.features[-1]
        else:
            self.target_layer = target_layer
            
        self._register_hooks()
        
    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output
            
        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0]
            
        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_full_backward_hook(backward_hook)
        
    def generate_heatmap(self, input_tensor, target_class_idx=None):
        """
        Generates Grad-CAM heatmap normalized to [0, 1].
        """
        self.model.zero_grad()
        output = self.model(input_tensor)
        
        if target_class_idx is None:
            target_class_idx = torch.argmax(output, dim=1).item()
            
        # Target score for backpropagation
        score = output[0, target_class_idx]
        score.backward(retain_graph=True)
        
        # Global Average Pooling on gradients
        weights = torch.mean(self.gradients, dim=(2, 3), keepdim=True)
        
        # Weighted combination of forward activation maps
        cam = torch.sum(weights * self.activations, dim=1, keepdim=True)
        
        # ReLU on weighted activation map (only positive influence contributes to class)
        cam = F.relu(cam)
        
        # Upsample to input dimensions (224, 224)
        cam = F.interpolate(cam, size=(input_tensor.shape[2], input_tensor.shape[3]), mode='bilinear', align_corners=False)
        
        cam = cam.squeeze().detach().cpu().numpy()
        cam = (cam - np.min(cam)) / (np.max(cam) - np.min(cam) + 1e-8)
        
        return cam, target_class_idx, output

def generate_gradcam_explanation(image_path, 
                                 model_path="best_model.pth", 
                                 class_indices_path="class_indices.json",
                                 output_path="gradcam_explanation.png"):
    """
    Generates a 3-panel explainability figure:
    Panel 1: Original Leaf Image
    Panel 2: Grad-CAM Saliency Heatmap
    Panel 3: Overlay on Original Leaf Image
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")
        
    idx_to_class = load_class_indices(class_indices_path)
    model = load_prediction_model(model_path=model_path, num_classes=len(idx_to_class), device="cpu")
    
    # Load and preprocess image
    raw_img = Image.open(image_path).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    input_tensor = transform(raw_img).unsqueeze(0)
    
    gradcam = GradCAM(model)
    heatmap, pred_idx, logits = gradcam.generate_heatmap(input_tensor)
    
    probs = F.softmax(logits[0], dim=0).detach().cpu().numpy()
    pred_class = idx_to_class[pred_idx]
    confidence = probs[pred_idx] * 100
    
    # Convert raw image to resized numpy for overlay
    raw_resized = raw_img.resize((224, 224))
    raw_np = np.array(raw_resized) / 255.0
    
    # Colormap
    cmap = plt.cm.jet
    heatmap_colored = cmap(heatmap)[:, :, :3]
    overlay = 0.55 * raw_np + 0.45 * heatmap_colored
    overlay = np.clip(overlay, 0, 1)
    
    # Create 3-panel visualization
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(raw_resized)
    axes[0].set_title("1. Input Farm Leaf Image", fontsize=12, fontweight='bold')
    axes[0].axis('off')
    
    im1 = axes[1].imshow(heatmap, cmap='jet')
    axes[1].set_title("2. Grad-CAM Pathogen Saliency", fontsize=12, fontweight='bold')
    axes[1].axis('off')
    plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
    
    axes[2].imshow(overlay)
    axes[2].set_title(f"3. Explainable AI Overlay\n({pred_class}: {confidence:.1f}%)", fontsize=11, fontweight='bold', color='darkgreen')
    axes[2].axis('off')
    
    plt.suptitle("Edge AI Explainability: Lesion & Pathology Attribution", fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=200)
    plt.close()
    
    logging.info(f"Grad-CAM explainability artifact saved to: {output_path}")
    return {
        'prediction': pred_class,
        'confidence': float(confidence),
        'heatmap': heatmap,
        'output_path': output_path
    }

if __name__ == "__main__":
    sample_img = "PlantVillage/Tomato__Tomato_mosaic_virus/49a98ba1-a1b1-4d4b-85af-29aa6648fc64___PSU_CG 2292.JPG"
    if os.path.exists(sample_img):
        generate_gradcam_explanation(sample_img)
