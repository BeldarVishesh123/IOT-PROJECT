# 🌾 AgriEdge AI: Multimodal Edge AI & IoT Crop Health Intelligence System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red.svg)](https://pytorch.org/)
[![ONNX Runtime](https://img.shields.io/badge/ONNX-Optimized-brightgreen.svg)](https://onnxruntime.ai/)
[![Test Accuracy](https://img.shields.io/badge/Test%20Accuracy-97.06%25-success.svg)](https://github.com/BeldarVishesh123/IOT-PROJECT)
[![Streamlit](https://img.shields.io/badge/Web%20Dashboard-Streamlit-FF4B4B.svg)](https://streamlit.io/)

AgriEdge AI is a high-performance, embedded-ready **Edge AI and Multimodal IoT Phytopathology System** engineered for autonomous crop health monitoring, pathogen localization, and precision agronomic interventions in solanaceous crops (Tomato, Potato, Bell Pepper).

---

## 🌟 Key Highlights & Innovations

1. **Multimodal IoT Sensor Fusion**:
   - Fuses Edge Vision inference with live microclimate telemetry (**Temperature, Relative Humidity, Soil Moisture, Leaf Wetness, Solar Radiation**).
   - Evaluates epidemiological disease affinity rules and computes a real-time **Disease Risk Index (DRI)** ($0\text{--}100$).
   - Generates actionable **Agronomic Prescriptions** (chemical treatments, bio-controls, precision irrigation management).

2. **Embedded & Edge Optimization (Quantization & ONNX)**:
   - Backbone: **MobileNetV3-Large** (4.22M parameters, 109.5 M-MACs).
   - **Quantized to INT8 & ONNX Runtime**: Compressed model size from **16.3 MB down to 0.40 MB (40x reduction)**.
   - Inference Latency: **3.21 ms / frame (311.7 FPS on CPU)**.
   - Ultra-low energy consumption: **16.05 mJ / inference** (~3.3M inferences on a 3000 mAh battery).

3. **Explainable AI (Grad-CAM)**:
   - Real-time Gradient-Weighted Class Activation Mapping.
   - Highlights foliar lesions, necrotic rings, and chlorosis patterns to verify that predictions stem from genuine pathology, not background artifacts.

4. **In-Field Agricultural Robustness Benchmark (ARI)**:
   - Evaluated against 6 severe real-world field domain shifts (Direct Sun Glare, Dusk Light, Wind Motion Blur, Fog/Dew Condensation, CMOS Sensor Noise, Lens Dirt Occlusion).
   - Achieves an **80.0% resilience retention rate** under severe distortions.

---

## 📊 Performance & Evaluation Summary

### 15-Class Stratified Test Set Performance (3,094 Images)
- **Test Accuracy**: **97.06%**
- **Weighted Precision**: **0.9710**
- **Weighted Recall**: **0.9706**
- **Weighted F1-Score**: **0.9705**

### Edge Hardware Latency & Footprint Benchmark
| Runtime Engine | Model Size | Mean Latency | P95 Latency | Throughput | Peak RAM |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PyTorch FP32 (Base)** | 16.30 MB | 8.57 ms | 9.29 ms | 116.6 FPS | 718 MB |
| **PyTorch Dynamic INT8** | 12.73 MB | 8.62 ms | 9.33 ms | 116.0 FPS | 731 MB |
| **ONNX Runtime (Graph Optimized)** | **0.40 MB** | **3.21 ms** | **3.35 ms** | **311.7 FPS** | 787 MB |

---

## 🚀 Quick Start & Installation

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/BeldarVishesh123/IOT-PROJECT.git
cd IOT-PROJECT

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Extract Dataset (Zipped Archive Chunks)
```bash
python unzip_dataset.py
```
*(Automatically reassembles `PlantVillage.zip.part_*` chunks and extracts the `PlantVillage/` folder).*

---

## 💻 Running the System

### 1. Launch Interactive Streamlit Web Dashboard
```bash
streamlit run app.py
```

### 2. Run Single-Image Inference with Grad-CAM
```bash
python predict_image.py --image-path "PlantVillage/Tomato__Tomato_mosaic_virus/49a98ba1-a1b1-4d4b-85af-29aa6648fc64___PSU_CG 2292.JPG"
```

### 3. Run Edge Hardware Benchmarking
```bash
python edge_benchmarking.py
```

### 4. Run In-Field Robustness Stress Test
```bash
python robustness_stress_test.py
```

### 5. Evaluate Model on Stratified Test Set
```bash
python evaluate_model.py
```

---

## 📂 Project Architecture

```
IOT-PROJECT/
├── app.py                             # Interactive Streamlit Web Dashboard
├── best_model.pth                     # Trained MobileNetV3 FP32 Model Weights
├── class_indices.json                 # 15-Class Index Mapping
├── edge_benchmarking.py               # Edge Latency & Hardware Power Profiler
├── edge_benchmark_results.json        # Benchmark Metrics Log
├── evaluate_model.py                  # Test Evaluation & Confusion Matrix Generator
├── master_demo.py                     # Master Automation CLI Runner
├── model_mobilenetv3.onnx             # Optimized ONNX FP32 Model
├── model_quantized_int8.pth           # Dynamic INT8 Quantized PyTorch Model
├── model_torchscript.pt               # LibTorch C++ Exported Model
├── PlantVillage.zip.part_*            # Tracked Dataset Archive Chunks (<100MB)
├── predict_image.py                   # Single-Image Diagnostic Script
├── requirements.txt                   # Project Dependencies
├── robustness_stress_test.py          # Domain Shift & Perturbation Stress Tester
├── unzip_dataset.py                   # Automated Dataset Reassembly & Extractor
└── src/
    ├── dataset.py                     # Stratified Data Loader & Deduplication
    ├── eval.py                        # Evaluation Metrics & Plotting Functions
    ├── explainable_ai.py              # Grad-CAM Explainability Engine
    ├── iot_sensor_fusion.py           # Multimodal Telemetry Fusion & Prescriptions
    ├── model.py                       # MobileNetV3 Architecture Definition
    ├── predict.py                     # Core Inference & Logits Pipeline
    ├── quantization_export.py         # INT8, TorchScript & ONNX Exporter
    └── train.py                       # Training Loop & Early Stopping Engine
```

---

## 📜 License & Citation
Developed by **Beldar Vishesh** for Smart Agriculture, Edge AI, and IoT Environmental Sensing.
Released under the MIT License.
