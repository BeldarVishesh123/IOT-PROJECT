import os
import sys
import json
import logging
import torch
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import torchvision.transforms as transforms
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.dataset import get_dataloaders
from src.predict import load_prediction_model, load_class_indices

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Agricultural Domain Shift Perturbation Operators ---
def apply_sun_glare(pil_img, factor=1.45):
    """Simulates harsh direct midday tropical sunlight & overexposure."""
    enhancer = ImageEnhance.Brightness(pil_img)
    img = enhancer.enhance(factor)
    enhancer_c = ImageEnhance.Contrast(img)
    return enhancer_c.enhance(1.20)

def apply_dusk_overcast(pil_img, factor=0.55):
    """Simulates dusk, cloud cover, and underexposed farm conditions."""
    enhancer = ImageEnhance.Brightness(pil_img)
    img = enhancer.enhance(factor)
    enhancer_c = ImageEnhance.Contrast(img)
    return enhancer_c.enhance(0.85)

def apply_wind_motion_blur(pil_img):
    """Simulates wind-induced crop motion blur."""
    return pil_img.filter(ImageFilter.BoxBlur(radius=3))

def apply_lens_dew_fog(pil_img):
    """Simulates morning condensation and greenhouse mist/fog on lens."""
    return pil_img.filter(ImageFilter.GaussianBlur(radius=2.5))

def apply_sensor_noise(pil_img, sigma=25):
    """Simulates low-cost IoT CMOS sensor noise (e.g. ESP32-CAM / low-light noise)."""
    np_img = np.array(pil_img, dtype=np.float32)
    noise = np.random.normal(0, sigma, np_img.shape)
    noisy = np.clip(np_img + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy)

def apply_lens_dirt_occlusion(pil_img, num_spots=4):
    """Simulates dirt spots, dust, and raindrops occluding parts of the lens."""
    np_img = np.array(pil_img).copy()
    h, w, _ = np_img.shape
    for _ in range(num_spots):
        spot_size = np.random.randint(12, 28)
        y = np.random.randint(0, h - spot_size)
        x = np.random.randint(0, w - spot_size)
        # Add semi-dark dirt patch
        np_img[y:y+spot_size, x:x+spot_size, :] = np.random.randint(30, 70, (spot_size, spot_size, 3))
    return Image.fromarray(np_img)

CORRUPTIONS = {
    "1. Baseline (Clean Pristine)": lambda img: img,
    "2. Blazing Sunlight (Overexposed)": apply_sun_glare,
    "3. Dusk / Overcast (Low-light)": apply_dusk_overcast,
    "4. Wind Motion Blur": apply_wind_motion_blur,
    "5. Lens Fog / Dew Condensation": apply_lens_dew_fog,
    "6. Low-Cost IoT Sensor Noise": apply_sensor_noise,
    "7. Lens Dirt / Raindrop Occlusion": apply_lens_dirt_occlusion
}

def evaluate_robustness_stress_test(dataset_dir="PlantVillage", 
                                    model_path="best_model.pth", 
                                    class_indices_path="class_indices.json",
                                    max_samples_per_corruption=300,
                                    output_dir="."):
    """
    Evaluates model resilience under synthetic real-world agricultural visual domain shifts.
    """
    logging.info("Starting Agricultural Real-World Domain Shift & Robustness Stress Test...")
    idx_to_class = load_class_indices(class_indices_path)
    model = load_prediction_model(model_path=model_path, num_classes=len(idx_to_class), device="cpu")
    model.eval()
    
    # Get test dataset
    _, _, test_loader, _ = get_dataloaders(dataset_dir=dataset_dir, batch_size=32)
    test_dataset = test_loader.dataset
    
    # Subsample test set for fast comprehensive evaluation
    total_test = len(test_dataset)
    eval_indices = np.random.RandomState(42).choice(
        total_test, min(max_samples_per_corruption, total_test), replace=False
    )
    
    base_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    results = {}
    corruption_names = []
    accuracies = []
    
    for c_name, c_func in CORRUPTIONS.items():
        correct = 0
        total = len(eval_indices)
        
        with torch.no_grad():
            for idx in eval_indices:
                img_path = test_dataset.image_paths[idx]
                label = test_dataset.labels[idx]
                
                # Load PIL image and apply corruption
                raw_img = Image.open(img_path).convert('RGB')
                corrupted_img = c_func(raw_img)
                
                # Transform and run inference
                tensor = base_transform(corrupted_img).unsqueeze(0)
                outputs = model(tensor)
                pred = torch.argmax(outputs, dim=1).item()
                
                if pred == label:
                    correct += 1
                    
        acc = (correct / total) * 100.0
        results[c_name] = {
            "evaluated_samples": total,
            "correct_predictions": correct,
            "accuracy_pct": round(acc, 2),
            "performance_status": "STABLE" if acc >= 85.0 else ("DEGRADED" if acc >= 70.0 else "VULNERABLE")
        }
        corruption_names.append(c_name.split(". ")[-1])
        accuracies.append(acc)
        logging.info(f"[{c_name}] -> Accuracy: {acc:.2f}% | Status: {results[c_name]['performance_status']}")

    # Calculate Agricultural Robustness Index (ARI = Average accuracy across all real-world perturbations)
    perturbed_accs = accuracies[1:] # Exclude pristine baseline
    mean_perturbed_acc = float(np.mean(perturbed_accs))
    baseline_acc = accuracies[0]
    retention_rate = (mean_perturbed_acc / max(baseline_acc, 1e-4)) * 100.0
    
    summary = {
        "baseline_accuracy_pct": round(baseline_acc, 2),
        "mean_perturbed_accuracy_pct": round(mean_perturbed_acc, 2),
        "agricultural_robustness_index_ari": round(mean_perturbed_acc, 2),
        "accuracy_retention_rate_pct": round(retention_rate, 2),
        "corruption_breakdown": results
    }
    
    # Save JSON Report
    json_path = os.path.join(output_dir, "robustness_evaluation_results.json")
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=4)
        
    # Generate Visualization Curve
    plt.figure(figsize=(11, 6))
    colors = ['#2ca02c' if a >= 85 else ('#ff7f0e' if a >= 70 else '#d62728') for a in accuracies]
    bars = plt.barh(corruption_names, accuracies, color=colors, edgecolor='black', alpha=0.85)
    plt.axvline(x=baseline_acc, color='blue', linestyle='--', linewidth=1.5, label=f'Baseline Accuracy ({baseline_acc:.1f}%)')
    plt.axvline(x=mean_perturbed_acc, color='purple', linestyle=':', linewidth=2, label=f'Mean Robustness Index ({mean_perturbed_acc:.1f}%)')
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 1.2, bar.get_y() + bar.get_height()/2, f"{width:.1f}%", va='center', fontweight='bold')
        
    plt.xlim(0, 115)
    plt.xlabel('Accuracy (%)', fontsize=12, fontweight='bold')
    plt.title('Agricultural IoT Robustness Benchmark: Model Resilience Under In-Field Perturbations', fontsize=13, fontweight='bold')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.legend(loc='lower left', frameon=True)
    plt.tight_layout()
    
    plot_path = os.path.join(output_dir, "robustness_curve.png")
    plt.savefig(plot_path, dpi=200)
    plt.close()
    logging.info(f"Robustness chart saved to: {plot_path}")
    
    # Print Terminal Table
    print("\n" + "="*75)
    print("AGRICULTURAL IN-FIELD DOMAIN SHIFT & ROBUSTNESS STRESS REPORT")
    print("="*75)
    print(f"Clean Baseline Accuracy: {baseline_acc:.2f}%")
    print(f"Mean Perturbed Accuracy (ARI): {mean_perturbed_acc:.2f}%")
    print(f"Resilience Retention Rate: {retention_rate:.1f}%")
    print("-"*75)
    for c_name, data in results.items():
        print(f"{c_name:<40} | Accuracy: {data['accuracy_pct']:6.2f}% | Status: {data['performance_status']}")
    print("="*75 + "\n")
    
    return summary

if __name__ == "__main__":
    evaluate_robustness_stress_test()
