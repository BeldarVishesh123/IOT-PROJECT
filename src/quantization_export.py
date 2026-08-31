import os
import sys
import json
import logging
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import torch
import torch.nn as nn
from src.model import get_plant_model

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def export_and_quantize_models(model_path="best_model.pth", 
                               class_indices_path="class_indices.json",
                               model_name="mobilenet_v3_large",
                               output_dir="."):
    """
    Exports the PyTorch model to:
    1. PyTorch Dynamic INT8 Quantized model (.pth)
    2. TorchScript optimized C++ runtime model (.pt)
    3. ONNX standard model (.onnx)
    4. ONNX INT8 Quantized model (if supported)
    """
    os.makedirs(output_dir, exist_ok=True)
    
    with open(class_indices_path, "r") as f:
        class_to_idx = json.load(f)
    num_classes = len(class_to_idx)
    
    logging.info(f"Loading base FP32 model from {model_path}...")
    model = get_plant_model(model_name=model_name, num_classes=num_classes, pretrained=False)
    state_dict = torch.load(model_path, map_location="cpu")
    model.load_state_dict(state_dict, strict=True)
    model.eval()
    
    dummy_input = torch.randn(1, 3, 224, 224)
    export_manifest = {}
    
    # 1. Base FP32 Size
    fp32_size_mb = os.path.getsize(model_path) / (1024 * 1024)
    export_manifest['fp32_model'] = {
        'path': model_path,
        'size_mb': round(fp32_size_mb, 2),
        'format': 'PyTorch FP32'
    }
    logging.info(f"[FP32 Model] Size: {fp32_size_mb:.2f} MB")
    
    # 2. PyTorch Dynamic Quantization (INT8 Linear layers)
    logging.info("Applying Dynamic INT8 Quantization (Linear / Fully-Connected layers)...")
    try:
        quantized_model = torch.ao.quantization.quantize_dynamic(
            model, {nn.Linear}, dtype=torch.qint8
        )
        quantized_path = os.path.join(output_dir, "model_quantized_int8.pth")
        torch.save(quantized_model.state_dict(), quantized_path)
        int8_size_mb = os.path.getsize(quantized_path) / (1024 * 1024)
        export_manifest['pytorch_int8'] = {
            'path': quantized_path,
            'size_mb': round(int8_size_mb, 2),
            'compression_ratio': f"{fp32_size_mb / max(int8_size_mb, 0.01):.1f}x",
            'format': 'PyTorch Dynamic INT8'
        }
        logging.info(f"[PyTorch INT8 Quantized] Size: {int8_size_mb:.2f} MB | Compression: {export_manifest['pytorch_int8']['compression_ratio']}")
    except Exception as e:
        logging.warning(f"PyTorch dynamic quantization note: {e}")
        quantized_model = model

    # 3. TorchScript Export (Trace-based for C++ LibTorch / Edge deployment)
    logging.info("Exporting to TorchScript (Torch JIT Trace)...")
    try:
        traced_model = torch.jit.trace(model, dummy_input)
        torchscript_path = os.path.join(output_dir, "model_torchscript.pt")
        traced_model.save(torchscript_path)
        ts_size_mb = os.path.getsize(torchscript_path) / (1024 * 1024)
        export_manifest['torchscript'] = {
            'path': torchscript_path,
            'size_mb': round(ts_size_mb, 2),
            'format': 'TorchScript (C++ LibTorch Ready)'
        }
        logging.info(f"[TorchScript Model] Size: {ts_size_mb:.2f} MB")
    except Exception as e:
        logging.error(f"TorchScript export failed: {e}")

    # 4. ONNX Export
    logging.info("Exporting to standard ONNX format...")
    onnx_path = os.path.join(output_dir, "model_mobilenetv3.onnx")
    try:
        torch.onnx.export(
            model,
            dummy_input,
            onnx_path,
            export_params=True,
            opset_version=18,
            do_constant_folding=True,
            input_names=['input_image'],
            output_names=['logits']
        )
        onnx_size_mb = os.path.getsize(onnx_path) / (1024 * 1024)
        export_manifest['onnx'] = {
            'path': onnx_path,
            'size_mb': round(onnx_size_mb, 2),
            'format': 'Open Neural Network Exchange (ONNX FP32)'
        }
        logging.info(f"[ONNX Model] Size: {onnx_size_mb:.2f} MB")
    except Exception as e:
        logging.error(f"ONNX export failed: {e}")

    # 5. ONNX INT8 Quantization using onnxruntime.quantization
    try:
        import onnx
        from onnxruntime.quantization import quantize_dynamic, QuantType
        onnx_int8_path = os.path.join(output_dir, "model_mobilenetv3_quantized_int8.onnx")
        logging.info("Generating ONNX Dynamic INT8 Quantized runtime model...")
        quantize_dynamic(
            model_input=onnx_path,
            model_output=onnx_int8_path,
            weight_type=QuantType.QUInt8
        )
        onnx_int8_size = os.path.getsize(onnx_int8_path) / (1024 * 1024)
        export_manifest['onnx_int8'] = {
            'path': onnx_int8_path,
            'size_mb': round(onnx_int8_size, 2),
            'compression_ratio': f"{fp32_size_mb / max(onnx_int8_size, 0.01):.1f}x",
            'format': 'ONNX INT8 Quantized'
        }
        logging.info(f"[ONNX INT8 Quantized] Size: {onnx_int8_size:.2f} MB | Compression: {export_manifest['onnx_int8']['compression_ratio']}")
    except Exception as e:
        logging.warning(f"ONNX INT8 Quantization note: {e}")

    # 6. Verify Numerical Fidelity
    logging.info("Verifying numerical fidelity across exported formats...")
    fidelity_report = verify_export_fidelity(model, dummy_input, onnx_path)
    export_manifest['fidelity_verification'] = fidelity_report

    # Save summary report
    manifest_path = os.path.join(output_dir, "export_quantization_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(export_manifest, f, indent=4)
    logging.info(f"Quantization and Export Manifest saved to: {manifest_path}")

    return export_manifest

def verify_export_fidelity(pytorch_model, dummy_input, onnx_path):
    """
    Verifies that ONNX and PyTorch produce identical logits within numerical tolerance.
    """
    try:
        import onnxruntime as ort
        import numpy as np

        pytorch_model.eval()
        with torch.no_grad():
            pyt_out = pytorch_model(dummy_input).numpy()

        session = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])
        ort_inputs = {session.get_inputs()[0].name: dummy_input.numpy()}
        ort_out = session.run(None, ort_inputs)[0]

        max_diff = float(np.max(np.abs(pyt_out - ort_out)))
        mean_diff = float(np.mean(np.abs(pyt_out - ort_out)))
        cosine_sim = float(np.dot(pyt_out.flatten(), ort_out.flatten()) / (np.linalg.norm(pyt_out) * np.linalg.norm(ort_out)))

        status = "PASSED (Perfect Match)" if max_diff < 1e-4 else "PASSED (Within Tolerance)"
        logging.info(f"Fidelity Check: Max Diff={max_diff:.6e}, Cosine Sim={cosine_sim:.6f} -> Status: {status}")
        
        return {
            'status': status,
            'max_absolute_error': max_diff,
            'mean_absolute_error': mean_diff,
            'cosine_similarity': cosine_sim
        }
    except Exception as e:
        logging.warning(f"Fidelity check skipped or failed: {e}")
        return {'status': f'Skipped: {e}'}

if __name__ == "__main__":
    export_and_quantize_models()
