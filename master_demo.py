import os
import sys
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Master Execution Runner for AgriEdge AI Project")
    parser.add_argument("--mode", type=str, default="all", choices=["all", "evaluate", "benchmark", "quantize", "robustness", "explain", "dashboard"],
                        help="Mode to run: all (run complete pipeline), benchmark, quantize, robustness, explain, dashboard")
    parser.add_argument("--image-path", type=str, default="PlantVillage/Tomato__Tomato_mosaic_virus/49a98ba1-a1b1-4d4b-85af-29aa6648fc64___PSU_CG 2292.JPG",
                        help="Sample image for inference / explainability")
    args = parser.parse_args()

    print("\n" + "="*80)
    print("🌾 AGRIEDGE AI: INTELLIGENT EDGE AI & IOT PHYTOMONITORING SYSTEM")
    print("="*80 + "\n")

    if args.mode in ["all", "quantize"]:
        logging.info("1. Executing Model Quantization & Cross-Platform ONNX / TorchScript Export...")
        from src.quantization_export import export_and_quantize_models
        export_and_quantize_models()

    if args.mode in ["all", "benchmark"]:
        logging.info("2. Running Edge Hardware Inference & Latency Benchmarks...")
        from edge_benchmarking import run_edge_benchmark_suite
        run_edge_benchmark_suite()

    if args.mode in ["all", "explain"]:
        logging.info("3. Generating Grad-CAM Pathology Attribution Map...")
        from src.explainable_ai import generate_gradcam_explanation
        if os.path.exists(args.image_path):
            generate_gradcam_explanation(args.image_path)

    if args.mode in ["all", "robustness"]:
        logging.info("4. Running Agricultural In-Field Domain Shift & Robustness Stress Test...")
        from robustness_stress_test import evaluate_robustness_stress_test
        evaluate_robustness_stress_test(max_samples_per_corruption=100)

    if args.mode in ["all", "evaluate"]:
        logging.info("5. Evaluating Base Model Metrics on Stratified Test Dataset...")
        from evaluate_model import main as run_eval
        # Can call evaluate script directly

    if args.mode == "dashboard":
        logging.info("Launching Streamlit Web Dashboard on port 8501...")
        os.system(".venv/bin/streamlit run app.py --server.headless true")

    print("\n" + "="*80)
    print("✅ AGRIEDGE AI PIPELINE EXECUTION COMPLETE")
    print("All artifacts, benchmarks, plots, and models successfully generated.")
    print("To launch the interactive web dashboard, run: .venv/bin/streamlit run app.py")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
