import os
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.formatting.rule import DataBarRule, CellIsRule
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.utils import get_column_letter

# Ensure correct working directory
target_dir = "/home/beldar-vishesh/Desktop/IOT project "
os.makedirs(target_dir, exist_ok=True)
os.chdir(target_dir)

wb = Workbook()
# Remove default sheet
wb.remove(wb.active)

# Define styles
NAVY_BLUE = "1F3864"
MEDIUM_BLUE = "2E5FA1"
LIGHT_BLUE = "D6E4F0"
GREEN_FILL = "C6EFCE"
YELLOW_FILL = "FFEB9C"
RED_FILL = "FFC7CE"
REC_BLUE_FILL = "BDD7EE"
GRAY_FILL = "F2F2F2"
WHITE_FILL = "FFFFFF"

title_font = Font(name='Calibri', size=16, bold=True, color="FFFFFF")
subtitle_font = Font(name='Calibri', size=12, bold=True, color="FFFFFF")
header_font = Font(name='Calibri', size=11, bold=True, color="FFFFFF")
section_font = Font(name='Calibri', size=11, bold=True, color="000000")
data_font = Font(name='Calibri', size=10)

title_fill = PatternFill(start_color=NAVY_BLUE, end_color=NAVY_BLUE, fill_type="solid")
header_fill = PatternFill(start_color=MEDIUM_BLUE, end_color=MEDIUM_BLUE, fill_type="solid")
section_fill = PatternFill(start_color=LIGHT_BLUE, end_color=LIGHT_BLUE, fill_type="solid")
alt_fill = PatternFill(start_color=GRAY_FILL, end_color=GRAY_FILL, fill_type="solid")
white_fill = PatternFill(start_color=WHITE_FILL, end_color=WHITE_FILL, fill_type="solid")

green_fill = PatternFill(start_color=GREEN_FILL, end_color=GREEN_FILL, fill_type="solid")
yellow_fill = PatternFill(start_color=YELLOW_FILL, end_color=YELLOW_FILL, fill_type="solid")
red_fill = PatternFill(start_color=RED_FILL, end_color=RED_FILL, fill_type="solid")
rec_blue_fill = PatternFill(start_color=REC_BLUE_FILL, end_color=REC_BLUE_FILL, fill_type="solid")

thin_border = Border(left=Side(style='thin', color='B4B4B4'),
                     right=Side(style='thin', color='B4B4B4'),
                     top=Side(style='thin', color='B4B4B4'),
                     bottom=Side(style='thin', color='B4B4B4'))

align_center = Alignment(horizontal="center", vertical="top", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="top", wrap_text=True)

def apply_base_formatting(ws, title, subtitle):
    ws.merge_cells('A1:J1')
    ws['A1'] = title
    ws['A1'].font = title_font
    ws['A1'].fill = title_fill
    ws['A1'].alignment = align_center

    ws.merge_cells('A2:J2')
    ws['A2'] = subtitle
    ws['A2'].font = subtitle_font
    ws['A2'].fill = title_fill
    ws['A2'].alignment = align_center

    ws['A3'] = "Last Updated: July 2026"
    ws['A3'].font = data_font

def format_data_row(ws, row_idx, start_col=1, end_col=10, is_alt=False):
    fill = alt_fill if is_alt else white_fill
    for col in range(start_col, end_col + 1):
        cell = ws.cell(row=row_idx, column=col)
        cell.font = data_font
        cell.border = thin_border
        cell.alignment = align_left
        if cell.fill.fill_type is None or cell.fill.start_color.rgb in ['00000000', 'FFFFFFFF']:
             cell.fill = fill

def format_header_row(ws, row_idx, start_col=1, end_col=10):
    for col in range(start_col, end_col + 1):
        cell = ws.cell(row=row_idx, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        cell.alignment = align_center

def format_section_header(ws, row_idx, text, start_col=1, end_col=10):
    ws.merge_cells(start_row=row_idx, start_column=start_col, end_row=row_idx, end_column=end_col)
    cell = ws.cell(row=row_idx, column=start_col)
    cell.value = text
    cell.font = section_font
    cell.fill = section_fill
    cell.border = thin_border
    cell.alignment = align_left

def adjust_col_widths(ws, cols_info):
    for col_letter, width in cols_info.items():
        ws.column_dimensions[col_letter].width = width


# --- SHEET 1: Executive Dashboard ---
ws1 = wb.create_sheet("1. Executive Dashboard")
apply_base_formatting(ws1, "PLANT DISEASE DETECTION USING EDGE AI AND IoT", "Executive Dashboard | Hardware Selection & Deployment Analysis")
format_section_header(ws1, 5, "PROJECT OVERVIEW", 1, 10)

overview_data = [
    ("Project", "Plant Disease Detection Using Edge AI and IoT"),
    ("Model Architecture", "MobileNetV3 Large (Transfer Learning)"),
    ("Framework", "PyTorch 2.x"),
    ("Dataset Classes", "15 plant disease/healthy classes"),
    ("Validated Test Accuracy", "97.19%"),
    ("Deployment Target", "Edge AI device with camera input")
]

for i, (k, v) in enumerate(overview_data):
    r = 7 + i
    ws1.cell(row=r, column=1, value=k)
    ws1.cell(row=r, column=2, value=v)
    ws1.merge_cells(start_row=r, start_column=2, end_row=r, end_column=10)
    format_data_row(ws1, r, 1, 10, is_alt=(i%2==1))
    ws1.cell(row=r, column=1).font = Font(name='Calibri', size=10, bold=True)

format_section_header(ws1, 14, "MODEL PERFORMANCE KPIs", 1, 10)
kpis = [
    ("Test Accuracy\n97.19%", 1),
    ("Weighted Precision\n97.22%", 3),
    ("Weighted Recall\n97.19%", 5),
    ("Weighted F1\n97.19%", 7)
]
for text, col in kpis:
    ws1.merge_cells(start_row=16, start_column=col, end_row=19, end_column=col+1)
    cell = ws1.cell(row=16, column=col)
    cell.value = text
    cell.font = Font(name='Calibri', size=12, bold=True)
    cell.fill = green_fill
    cell.alignment = align_center
    cell.border = thin_border

format_section_header(ws1, 21, "TOP RECOMMENDATIONS", 1, 10)
rec_headers = ["Category", "Recommended Device", "Score", "Key Reason"]
for i, h in enumerate(rec_headers):
    ws1.cell(row=23, column=i*2+1, value=h)
    ws1.merge_cells(start_row=23, start_column=i*2+1, end_row=23, end_column=i*2+2)
format_header_row(ws1, 23, 1, 8)

recs_data = [
    ("Best Overall", "Jetson Orin Nano Super Dev Kit", "92/100", "Native PyTorch+CUDA, 67 TOPS, $249"),
    ("Best Budget", "Raspberry Pi 5 (8GB)", "68/100", "Affordable, PyTorch CPU, good ecosystem"),
    ("Best Performance", "Jetson AGX Orin", "85/100", "275 TOPS, 32GB RAM, overkill but powerful"),
    ("Best Low-Power", "Coral USB + RPi 5", "65/100", "4 TOPS Edge TPU, low power, needs conversion"),
    ("Best IoT Capture", "ESP32-CAM", "N/A", "Camera+Wi-Fi for image capture only, no ML"),
    ("Best Scalability", "Jetson Orin Nano Super", "92/100", "Upgradeable, NVIDIA ecosystem, JetPack")
]

for i, row_data in enumerate(recs_data):
    r = 24 + i
    for j, val in enumerate(row_data):
        ws1.cell(row=r, column=j*2+1, value=val)
        ws1.merge_cells(start_row=r, start_column=j*2+1, end_row=r, end_column=j*2+2)
    format_data_row(ws1, r, 1, 8, is_alt=(i%2==1))

format_section_header(ws1, 30, "RECOMMENDED SYSTEM ARCHITECTURE", 1, 10)
architecture_text = """Plant Leaf
-> Camera Module (CSI/USB)
-> NVIDIA Jetson Orin Nano Super
-> Image Preprocessing (OpenCV)
-> MobileNetV3 Large Inference (PyTorch/TensorRT)
-> Disease Classification (15 classes)
-> Confidence Score + Result Display
-> Optional: Wi-Fi -> IoT Dashboard / Cloud"""
ws1.merge_cells('A32:J38')
cell = ws1.cell(row=32, column=1)
cell.value = architecture_text
cell.font = data_font
cell.alignment = align_left
cell.border = thin_border
cell.fill = white_fill

format_section_header(ws1, 40, "SHEET NAVIGATION", 1, 10)
sheets = [
    "2. Project Requirements", "3. Edge AI vs IoT", "4. System Architecture",
    "5. Device Comparison", "6. Price & Total Cost", "7. Hardware Specifications",
    "8. Software Compatibility", "9. ML Model Deployment", "10. Performance & AI",
    "11. Power & Deployment", "12. Device Analysis", "13. Decision Matrix",
    "14. Final Recommendation", "15. Sources & References"
]
for i, s in enumerate(sheets):
    r = 42 + i
    ws1.cell(row=r, column=1).hyperlink = f"#'{s}'!A1"
    ws1.cell(row=r, column=1).value = s
    ws1.cell(row=r, column=1).font = Font(name='Calibri', size=11, color="0563C1", underline="single")
    ws1.merge_cells(start_row=r, start_column=1, end_row=r, end_column=10)

ws1.cell(row=58, column=1, value="Disclaimer: Prices and availability are approximate and may vary by region and supplier. Verify current pricing before purchase.")
ws1.merge_cells('A58:J58')
ws1.cell(row=58, column=1).font = Font(name='Calibri', size=9, italic=True)

adjust_col_widths(ws1, {'A':15, 'B':20, 'C':15, 'D':25, 'E':15, 'F':20, 'G':15, 'H':30, 'I':10, 'J':10})


# --- SHEET 2: Project Requirements ---
ws2 = wb.create_sheet("2. Project Requirements")
apply_base_formatting(ws2, "PROJECT REQUIREMENTS", "Analysis of Needs and Evaluation Methods")
ws2.freeze_panes = "A5"

req_headers = ["S.No.", "Requirement", "Priority (Critical/High/Medium/Low)", "Why It Matters", "Minimum Requirement", "Preferred Requirement", "Evaluation Method"]
for i, h in enumerate(req_headers):
    ws2.cell(row=4, column=i+1, value=h)
format_header_row(ws2, 4, 1, len(req_headers))

req_data = [
    [1, "Image Classification", "Critical", "Core project function", "Classify plant leaf images", "Real-time classification", "Test with sample images"],
    [2, "MobileNetV3 Large Support", "Critical", "Current trained model architecture", "Must load model", "Native PyTorch loading", "Load .pth and verify output"],
    [3, "PyTorch Framework", "Critical", "Model is trained in PyTorch", "PyTorch 1.x minimum", "PyTorch 2.x with GPU", "pip install torch, run inference"],
    [4, "GPU/CUDA Acceleration", "High", "Faster inference for real-time", "CPU-only acceptable", "CUDA GPU with TensorRT", "Benchmark inference time"],
    [5, "TensorRT Support", "Medium", "Optimized inference engine", "Not required", "TensorRT 8.x+", "Convert ONNX to TensorRT"],
    [6, "ONNX Support", "Medium", "Model portability", "Not required", "ONNX export + runtime", "Export .pth to .onnx"],
    [7, "OpenCV", "High", "Image capture and preprocessing", "OpenCV 4.x", "OpenCV with camera support", "Test camera feed"],
    [8, "Camera Support", "Critical", "Image input", "USB camera", "CSI camera interface", "Connect and test"],
    [9, "Real-Time Inference", "High", "Practical usability", "<5 seconds per image", "<500ms per image", "Benchmark FPS"],
    [10, "Local Inference", "Critical", "No internet dependency", "Process images locally", "Full offline operation", "Test without network"],
    [11, "Internet Independence", "High", "Field deployment", "Offline inference", "Full offline mode", "Disconnect and test"],
    [12, "Wi-Fi Connectivity", "Medium", "IoT data transmission", "Optional", "Built-in Wi-Fi", "Connect to network"],
    [13, "Bluetooth", "Low", "Optional connectivity", "Not required", "Built-in BT", "Pair device"],
    [14, "GPIO/Expansion", "Low", "Sensor integration", "Basic GPIO", "40-pin GPIO header", "Connect LED/sensor"],
    [15, "USB Ports", "High", "Camera, storage, peripherals", "1x USB", "2+ USB 3.0", "Connect peripherals"],
    [16, "Storage", "High", "OS, model, data", "16GB minimum", "64GB+ NVMe SSD", "Boot and store model"],
    [17, "RAM", "High", "Model loading, inference", "2GB minimum", "8GB+", "Load model + process"],
    [18, "Power Consumption", "Medium", "Portable deployment", "<25W", "<15W", "Measure with multimeter"],
    [19, "Portability", "Medium", "Field testing", "Compact form factor", "Small SBC", "Measure dimensions"],
    [20, "Cost", "High", "College project budget", "<INR 50,000", "<INR 30,000", "Compare prices"],
    [21, "Future IoT Integration", "Medium", "Project expansion", "Wi-Fi available", "MQTT/HTTP support", "Send data to cloud"],
    [22, "Scalability", "Low", "Future expansion", "Single camera", "Multi-camera, multi-model", "Test scaling"],
    [23, "Deployment Ease", "High", "Time-limited project", "Documentation available", "Complete SDK/toolkit", "Setup time"]
]
for i, row_data in enumerate(req_data):
    r = 5 + i
    for j, val in enumerate(row_data):
        ws2.cell(row=r, column=j+1, value=val)
    format_data_row(ws2, r, 1, len(req_headers), is_alt=(i%2==1))
adjust_col_widths(ws2, {'A':8, 'B':25, 'C':15, 'D':30, 'E':25, 'F':25, 'G':25})
ws2.auto_filter.ref = f"A4:G{len(req_data)+4}"


# --- SHEET 3: Edge AI vs IoT ---
ws3 = wb.create_sheet("3. Edge AI vs IoT")
apply_base_formatting(ws3, "EDGE AI VS IoT", "Conceptual Differences & Project Integration")
ws3.freeze_panes = "A5"

ws3_headers = ["Aspect", "Edge AI Device", "IoT Device"]
for i, h in enumerate(ws3_headers):
    ws3.cell(row=4, column=i+1, value=h)
format_header_row(ws3, 4, 1, len(ws3_headers))

ws3_data = [
    ["Definition", "Computing device that processes data locally near the source using AI/ML", "Connected physical device that collects/transmits data over a network"],
    ["Primary Purpose", "Local AI inference, real-time decision making", "Data collection, sensing, communication, actuation"],
    ["Data Processing Location", "On the device itself (at the edge)", "Primarily in the cloud or remote server"],
    ["AI/ML Capability", "Strong — can run neural networks locally", "Very limited or none (may run TinyML)"],
    ["CPU/GPU/NPU", "Powerful CPU + GPU/NPU (e.g., Jetson has CUDA GPU)", "Microcontroller-class CPU (e.g., ESP32 at 240MHz)"],
    ["Local Inference", "Yes — primary function", "No or extremely limited (TFLite Micro only)"],
    ["Cloud Dependency", "Low — operates independently", "High — often requires cloud for processing"],
    ["Internet Dependency", "Low — works offline for inference", "High — needs connectivity to function fully"],
    ["Latency", "Very low (milliseconds for local inference)", "Variable — depends on network (can be seconds)"],
    ["Bandwidth Usage", "Low — only sends results/summaries", "Can be high — may send raw sensor/image data"],
    ["Privacy", "High — data stays on device", "Lower — data transmitted to cloud"],
    ["Power Consumption", "Medium to High (5-60W depending on device)", "Very Low (0.5-2W typical)"],
    ["Hardware Complexity", "Higher — SBC with GPU, heatsink, storage", "Lower — simple MCU board"],
    ["Camera Capability", "Excellent — CSI + USB cameras, high-res", "Basic — low-res OV2640 type (ESP32-CAM)"],
    ["Sensor Capability", "Can interface sensors via GPIO/I2C/SPI", "Primary function — temp, humidity, soil moisture"],
    ["Connectivity", "Wi-Fi, Ethernet, USB, Bluetooth", "Wi-Fi, Bluetooth, LoRa, Zigbee, MQTT"],
    ["Typical Examples", "Jetson Orin Nano, Jetson AGX Orin, RPi 5", "ESP32, ESP32-CAM, Arduino + sensors"],
    ["Advantages", "Powerful local AI, low latency, privacy, offline", "Low cost, low power, many sensors, wide connectivity"],
    ["Disadvantages", "Higher cost, higher power, more complex setup", "Cannot run complex ML, cloud-dependent"],
    ["Cost Range", "$60 — $2000+", "$2 — $20"],
    ["Best Use Cases", "Image classification, object detection, autonomous systems", "Environmental monitoring, smart agriculture sensors"]
]
for i, row_data in enumerate(ws3_data):
    r = 5 + i
    for j, val in enumerate(row_data):
        ws3.cell(row=r, column=j+1, value=val)
    format_data_row(ws3, r, 1, 3, is_alt=(i%2==1))

format_section_header(ws3, 27, "HOW EDGE AI AND IoT WORK TOGETHER IN THIS PROJECT", 1, 3)
integration_text = """Edge AI and IoT are NOT competing concepts — they are complementary. In this project:
- The ESP32-CAM (IoT device) can capture plant images and transmit them via Wi-Fi
- The Jetson Orin Nano (Edge AI device) receives images and runs MobileNetV3 Large inference locally
- Environmental sensors (IoT) can provide additional context (temperature, humidity, soil moisture)
- Results can be sent to a cloud dashboard (IoT connectivity) for monitoring

Component Classification:
- IoT Components: ESP32-CAM, sensors, Wi-Fi modules, MQTT broker, cloud dashboard
- Edge AI Components: Jetson Orin Nano, camera, MobileNetV3 model, TensorRT engine
- AI/ML Components: MobileNetV3 Large, PyTorch, TensorRT, inference pipeline
- Communication: Wi-Fi, MQTT, HTTP/REST API
- Cloud/Software: Dashboard, database, alert system"""

ws3.merge_cells('A28:C38')
cell = ws3.cell(row=28, column=1)
cell.value = integration_text
cell.font = data_font
cell.alignment = align_left
cell.border = thin_border
cell.fill = white_fill

adjust_col_widths(ws3, {'A':25, 'B':45, 'C':45})


# --- SHEET 4: System Architecture ---
ws4 = wb.create_sheet("4. System Architecture")
apply_base_formatting(ws4, "SYSTEM ARCHITECTURE", "Data Flow and Component Breakdown")

format_section_header(ws4, 4, "OPTION A: EDGE AI ONLY (RECOMMENDED FOR DEMO)", 1, 4)
ws4_h1 = ["Step", "Component", "Type", "Description"]
for i, h in enumerate(ws4_h1):
    ws4.cell(row=5, column=i+1, value=h)
format_header_row(ws4, 5, 1, 4)

opt_a_data = [
    [1, "Plant Leaf", "Input", "Physical plant leaf with potential disease"],
    [2, "Camera Module (CSI/USB)", "Hardware", "Captures high-resolution image of leaf"],
    [3, "Jetson Orin Nano Super", "Edge AI Device", "Receives image for processing"],
    [4, "OpenCV Preprocessing", "Software", "Resize to 224x224, normalize, CenterCrop"],
    [5, "MobileNetV3 Large Model", "AI/ML", "PyTorch inference or TensorRT optimized"],
    [6, "Softmax Classification", "AI/ML", "Outputs probabilities for 15 classes"],
    [7, "Disease Name + Confidence", "Output", "Top prediction with confidence percentage"],
    [8, "Local Display/Terminal", "Output", "Shows result on connected display"]
]
for i, row_data in enumerate(opt_a_data):
    r = 6 + i
    for j, val in enumerate(row_data):
        ws4.cell(row=r, column=j+1, value=val)
    format_data_row(ws4, r, 1, 4, is_alt=(i%2==1))

format_section_header(ws4, 15, "OPTION B: EDGE AI + IoT (FULL SYSTEM)", 1, 4)
for i, h in enumerate(ws4_h1):
    ws4.cell(row=16, column=i+1, value=h)
format_header_row(ws4, 16, 1, 4)
opt_b_data = [
    [1, "Plant Leaf", "Input", "Physical plant leaf"],
    [2, "ESP32-CAM / USB Camera", "IoT/Hardware", "Captures image, sends via Wi-Fi"],
    [3, "Wi-Fi Network", "Communication", "Transmits image to edge device"],
    [4, "Jetson Orin Nano Super", "Edge AI Device", "Receives and processes image"],
    [5, "MobileNetV3 Large", "AI/ML", "Disease classification inference"],
    [6, "Disease Prediction", "Output", "Class name + confidence score"],
    [7, "MQTT / HTTP API", "Communication", "Sends result to cloud/dashboard"],
    [8, "Cloud Dashboard", "Software", "Web interface for monitoring"],
    [9, "Optional: Temp/Humidity Sensors", "IoT Sensors", "Environmental context data"],
    [10, "Optional: Mobile App Alert", "Software", "Push notification to farmer"]
]
for i, row_data in enumerate(opt_b_data):
    r = 17 + i
    for j, val in enumerate(row_data):
        ws4.cell(row=r, column=j+1, value=val)
    format_data_row(ws4, r, 1, 4, is_alt=(i%2==1))

format_section_header(ws4, 28, "COMPONENT CLASSIFICATION", 1, 4)
ws4_h2 = ["Component", "Category", "Role in System", ""]
for i, h in enumerate(ws4_h2[:3]):
    ws4.cell(row=29, column=i+1, value=h)
format_header_row(ws4, 29, 1, 3)
class_data = [
    ["Jetson Orin Nano Super", "Edge AI", "Primary AI inference device"],
    ["Camera (CSI/USB)", "Hardware Input", "Image capture"],
    ["MobileNetV3 Large", "AI/ML Model", "Disease classification"],
    ["PyTorch / TensorRT", "ML Framework", "Model inference engine"],
    ["OpenCV", "Software", "Image preprocessing"],
    ["ESP32-CAM", "IoT Device", "Remote image capture + Wi-Fi transmission"],
    ["Temperature Sensor", "IoT Sensor", "Environmental monitoring"],
    ["Humidity Sensor", "IoT Sensor", "Environmental monitoring"],
    ["Soil Moisture Sensor", "IoT Sensor", "Environmental monitoring"],
    ["Wi-Fi Module", "Communication", "Data transmission"],
    ["MQTT Broker", "Communication", "Message protocol"],
    ["Cloud Server", "Cloud", "Data storage and dashboard"],
    ["Web Dashboard", "Software", "User interface for results"]
]
for i, row_data in enumerate(class_data):
    r = 30 + i
    for j, val in enumerate(row_data):
        ws4.cell(row=r, column=j+1, value=val)
    format_data_row(ws4, r, 1, 3, is_alt=(i%2==1))

adjust_col_widths(ws4, {'A':10, 'B':35, 'C':25, 'D':45})


# --- SHEET 5: Device Comparison ---
ws5 = wb.create_sheet("5. Device Comparison")
apply_base_formatting(ws5, "DEVICE COMPARISON", "Comprehensive Feature Matrix for Edge AI Hardware")
ws5.freeze_panes = "A5"

ws5_headers = ["Device", "Category (SBC/Accelerator/MCU)", "Status (Active/EOL)", "Processor", "GPU/AI Accelerator", "RAM", "Storage", "CUDA", "PyTorch", "TensorFlow", "TensorRT", "ONNX", "TFLite", "OpenCV", "Camera (CSI/USB)", "Wi-Fi", "Bluetooth", "USB Ports", "GPIO", "Power (W)", "OS", "Edge AI Rating (1-5)", "IoT Rating (1-5)", "Deployment Difficulty", "Best Use Case", "Project Suitability", "Recommendation"]

for i, h in enumerate(ws5_headers):
    ws5.cell(row=4, column=i+1, value=h)
format_header_row(ws5, 4, 1, len(ws5_headers))

ws5_data = [
    ["Jetson Nano", "SBC", "EOL/Discontinued", "4x Cortex-A57", "128 Maxwell CUDA cores", "4GB LPDDR4", "MicroSD", "Yes (10.2)", "Yes (older 1.x)", "Yes (older)", "Yes (7.x)", "Yes", "Yes", "Yes", "CSI+USB", "No", "No", "4x USB 3.0", "40-pin", "5-10W", "Ubuntu 18.04", 3, 2, "Medium", "Legacy projects", "Not Recommended (EOL)", "Not Recommended"],
    ["Jetson Orin Nano", "SBC", "Active", "6x Cortex-A78AE", "1024 Ampere CUDA, 32 Tensor", "8GB LPDDR5", "NVMe SSD", "Yes (12.x)", "Yes (2.x)", "Yes", "Yes (8.x+)", "Yes", "Yes", "Yes", "CSI+USB", "No (add-on)", "No (add-on)", "USB 3.2", "40-pin", "7-15W", "Ubuntu 22.04", 5, 3, "Easy", "Edge AI inference", "Highly Recommended", "Highly Recommended"],
    ["Jetson Orin Nano Super", "SBC", "Active", "6x Cortex-A78AE", "1024 Ampere CUDA, 32 Tensor", "8GB LPDDR5", "NVMe SSD", "Yes (12.x)", "Yes (2.x)", "Yes", "Yes (8.x+)", "Yes", "Yes", "Yes", "CSI+USB", "No (add-on)", "No (add-on)", "USB 3.2", "40-pin", "7-25W", "Ubuntu 22.04", 5, 3, "Easy", "Edge AI inference (best value)", "Highly Recommended", "Highly Recommended"],
    ["Jetson AGX Orin", "SBC", "Active", "12x Cortex-A78AE", "2048 Ampere CUDA, 64 Tensor", "32GB LPDDR5", "64GB eMMC + NVMe", "Yes (12.x)", "Yes (2.x)", "Yes", "Yes (8.x+)", "Yes", "Yes", "Yes", "CSI+USB", "No (add-on)", "No (add-on)", "USB 3.2", "40-pin", "15-60W", "Ubuntu 22.04", 5, 3, "Easy", "High-perf edge AI", "Recommended (overkill)", "Recommended"],
    ["Coral Dev Board", "SBC", "EOL", "4x Cortex-A53 + M4F", "Google Edge TPU (4 TOPS)", "4GB LPDDR4", "8GB eMMC", "No", "No", "Partial", "No", "No", "Yes (required)", "Yes", "CSI+USB", "Yes", "Yes", "USB 2.0/3.0", "GPIO", "2-3W", "Mendel Linux", 3, 3, "Hard", "Low-power Edge TPU", "Possible (EOL risk)", "Possible"],
    ["Coral USB Accelerator", "Accelerator", "EOL", "N/A (requires host)", "Google Edge TPU (4 TOPS)", "N/A", "N/A", "No", "No", "Partial", "No", "No", "Yes (required)", "Yes", "Via host", "Via host", "Via host", "Via host", "Via host", "0.5W (TPU)", "Via host OS", 3, 2, "Hard", "Add-on AI for RPi/PC", "Possible (EOL risk)", "Possible"],
    ["Raspberry Pi 5", "SBC", "Active", "4x Cortex-A76 @2.4GHz", "VideoCore VII (no CUDA)", "4/8GB LPDDR4X", "MicroSD + NVMe HAT", "No", "Yes (CPU only)", "Yes (CPU)", "No", "Yes", "Yes", "Yes", "CSI+USB", "Yes (Wi-Fi 5)", "Yes (BT 5.0)", "2x USB3 + 2x USB2", "40-pin", "5-12W", "RPi OS/Ubuntu", 2, 4, "Easy", "Budget edge/IoT", "Recommended (budget)", "Recommended"],
    ["ESP32-CAM", "MCU", "Active", "2x Xtensa LX6 @240MHz", "None", "520KB SRAM+4MB PSRAM", "4MB Flash", "No", "No", "No", "No", "No", "Micro only", "Limited", "Built-in OV2640", "Yes", "Yes", "No USB host", "GPIO", "1-2W", "Arduino/FreeRTOS", 0, 5, "N/A for ML", "IoT image capture", "Not Recommended (no ML)", "Not Recommended"]
]

for i, row_data in enumerate(ws5_data):
    r = 5 + i
    for j, val in enumerate(row_data):
        cell = ws5.cell(row=r, column=j+1, value=val)
        if j == 26: # Recommendation column
            if "Highly" in val: cell.fill = green_fill
            elif "Recommended" in val and "Not" not in val: cell.fill = rec_blue_fill
            elif "Possible" in val: cell.fill = yellow_fill
            else: cell.fill = red_fill
    format_data_row(ws5, r, 1, len(ws5_headers), is_alt=(i%2==1))

cols_w = {get_column_letter(i+1): 18 for i in range(len(ws5_headers))}
cols_w['A'] = 25
cols_w['B'] = 20
cols_w['Y'] = 25
cols_w['Z'] = 25
cols_w['AA'] = 25
adjust_col_widths(ws5, cols_w)
ws5.auto_filter.ref = f"A4:AA{len(ws5_data)+4}"


# --- SHEET 6: Price & Total Cost Analysis ---
ws6 = wb.create_sheet("6. Price & Total Cost")
apply_base_formatting(ws6, "PRICE & TOTAL COST ANALYSIS", "Estimated Acquisition and Setup Costs in India")
ws6.freeze_panes = "A5"

ws6_headers = ["Device", "Official MSRP (USD)", "India Price (INR)", "Price Status", "Availability", "Camera Cost (INR)", "Power Supply (INR)", "Storage (INR)", "Cooling (INR)", "Other Accessories (INR)", "Est. Total Setup (INR)", "Price Source", "Price Date", "Reliability"]
for i, h in enumerate(ws6_headers):
    ws6.cell(row=4, column=i+1, value=h)
format_header_row(ws6, 4, 1, len(ws6_headers))

ws6_data = [
    ["Jetson Nano", "$149", "Variable (EOL)", "Discontinued", "Limited remaining stock", "2,000", "1,000", "500 (MicroSD)", "500", "500 (case)", "18,000-25,000", "nvidia.com", "Jul 2026", "Low"],
    ["Jetson Orin Nano", "$249", "30,000-75,000", "Active", "Available via distributors", "2,000", "Included in dev kit", "2,000 (NVMe SSD)", "1,000", "1,000", "36,000-81,000", "nvidia.com, Robocraze", "Jul 2026", "Medium"],
    ["Jetson Orin Nano Super", "$249", "30,000-75,000", "Active", "Available via distributors", "2,000", "Included in dev kit", "2,000 (NVMe SSD)", "1,000", "1,000", "36,000-81,000", "nvidia.com, Robocraze", "Jul 2026", "Medium"],
    ["Jetson AGX Orin", "$1,999", "2,00,000-3,00,000", "Active", "Via authorized distributors", "2,000", "Included", "Included (64GB eMMC)", "Included", "2,000", "2,04,000-3,04,000", "nvidia.com, ThinkRobotics", "Jul 2026", "Medium"],
    ["Coral Dev Board", "$130", "17,000-20,500", "EOL", "Limited remaining stock", "2,000", "1,000", "Included (8GB eMMC)", "Not needed", "1,000", "21,000-24,500", "coral.ai", "Jul 2026", "Low"],
    ["Coral USB + RPi 5", "$60+$80", "7,500-16,000 + 12,000-13,000", "EOL (Coral)", "Limited (Coral)", "2,000", "1,500", "1,000", "Not needed", "1,000", "25,000-33,500", "coral.ai, raspberrypi.com", "Jul 2026", "Low-Medium"],
    ["Raspberry Pi 5 (8GB)", "$80", "12,000-13,000", "Active", "Widely available", "2,000", "1,500", "1,000 (MicroSD)", "500 (optional fan)", "1,000 (case)", "18,000-19,000", "raspberrypi.com, Robu.in", "Jul 2026", "High"],
    ["ESP32-CAM", "$5-10", "200-800", "Active", "Widely available", "Included", "300", "Included", "Not needed", "200 (programmer)", "700-1,300", "espressif.com, Robu.in", "Jul 2026", "High"]
]
for i, row_data in enumerate(ws6_data):
    r = 5 + i
    for j, val in enumerate(row_data):
        ws6.cell(row=r, column=j+1, value=val)
    format_data_row(ws6, r, 1, len(ws6_headers), is_alt=(i%2==1))

ws6.cell(row=14, column=1, value="Disclaimer: Prices are approximate and fluctuate based on supply, import duties, and local Indian distributors.")
ws6.merge_cells('A14:N14')
ws6.cell(row=14, column=1).font = Font(name='Calibri', size=9, italic=True)

cols_w6 = {get_column_letter(i+1): 18 for i in range(len(ws6_headers))}
cols_w6['A'] = 25
cols_w6['K'] = 20
cols_w6['L'] = 25
adjust_col_widths(ws6, cols_w6)
ws6.auto_filter.ref = f"A4:N{len(ws6_data)+4}"


# --- SHEET 7: Hardware Specifications ---
ws7 = wb.create_sheet("7. Hardware Specifications")
apply_base_formatting(ws7, "HARDWARE SPECIFICATIONS", "Technical Details by Component")
ws7.freeze_panes = "B5"

ws7_headers = ["Specification", "Jetson Nano", "Jetson Orin Nano", "Jetson Orin Nano Super", "Jetson AGX Orin", "Coral Dev Board", "Coral USB Acc.", "Raspberry Pi 5", "ESP32-CAM"]
for i, h in enumerate(ws7_headers):
    ws7.cell(row=4, column=i+1, value=h)
format_header_row(ws7, 4, 1, len(ws7_headers))

ws7_data = [
    ["CPU", "4x Cortex-A57 @1.43GHz", "6x Cortex-A78AE", "6x Cortex-A78AE", "12x Cortex-A78AE", "4x Cortex-A53 + M4F", "N/A (host)", "4x Cortex-A76 @2.4GHz", "2x Xtensa LX6 @240MHz"],
    ["CPU Architecture", "ARMv8-A 64-bit", "ARMv8.2-A 64-bit", "ARMv8.2-A 64-bit", "ARMv8.2-A 64-bit", "ARMv8-A 64-bit", "N/A", "ARMv8.2-A 64-bit", "Xtensa 32-bit"],
    ["GPU", "128-core Maxwell", "1024-core Ampere", "1024-core Ampere", "2048-core Ampere", "None", "None", "VideoCore VII", "None"],
    ["GPU Architecture", "Maxwell", "Ampere", "Ampere", "Ampere", "N/A", "N/A", "Broadcom (no CUDA)", "N/A"],
    ["CUDA Cores", "128", "1024", "1024", "2048", "0", "0", "0", "0"],
    ["Tensor Cores", "0", "32", "32", "64", "0", "0", "0", "0"],
    ["AI Accelerator", "GPU (Maxwell)", "GPU (Ampere)", "GPU (Ampere)", "GPU (Ampere)", "Edge TPU", "Edge TPU", "None", "None"],
    ["AI Performance", "472 GFLOPS (FP16)", "40 TOPS (INT8)", "67 TOPS (INT8)", "275 TOPS (INT8)", "4 TOPS (INT8)", "4 TOPS (INT8)", "~30 GFLOPS (est.)", "Negligible"],
    ["RAM", "4GB LPDDR4", "8GB LPDDR5", "8GB LPDDR5", "32GB LPDDR5", "4GB LPDDR4", "N/A (host)", "4/8GB LPDDR4X", "520KB SRAM + 4MB PSRAM"],
    ["RAM Bandwidth", "25.6 GB/s", "68 GB/s", "68 GB/s", "204.8 GB/s", "14.9 GB/s", "N/A", "~32 GB/s", "N/A"],
    ["Storage", "MicroSD", "NVMe SSD (M.2)", "NVMe SSD (M.2)", "64GB eMMC + NVMe", "8GB eMMC + MicroSD", "N/A (host)", "MicroSD + NVMe HAT", "4MB Flash"],
    ["USB Ports", "4x USB 3.0, 1x USB 2.0 Micro", "4x USB 3.2 Gen2", "4x USB 3.2 Gen2", "4x USB 3.2 + USB-C", "USB 2.0 + USB 3.0", "USB 3.0 (connection)", "2x USB 3.0, 2x USB 2.0", "No USB host"],
    ["Display Output", "HDMI 2.0 + DP", "HDMI + DP", "HDMI + DP", "HDMI + DP", "HDMI", "Via host", "2x micro-HDMI", "No"],
    ["Camera Interface", "CSI (MIPI) + USB", "CSI (MIPI) + USB", "CSI (MIPI) + USB", "CSI (MIPI) + USB", "CSI (MIPI) + USB", "Via host", "CSI (MIPI) + USB", "Built-in OV2640"],
    ["Ethernet", "Gigabit", "Gigabit", "Gigabit", "10 Gigabit", "Gigabit", "Via host", "Gigabit", "No"],
    ["Wi-Fi", "No (add module)", "No (add module)", "No (add module)", "No (add module)", "802.11ac", "Via host", "Wi-Fi 5 (802.11ac)", "802.11b/g/n"],
    ["Bluetooth", "No (add module)", "No (add module)", "No (add module)", "No (add module)", "BT 4.2", "Via host", "BT 5.0 / BLE", "BT 4.2"],
    ["GPIO", "40-pin header", "40-pin header", "40-pin header", "40-pin header", "40-pin header", "N/A", "40-pin header", "GPIO pins"],
    ["Power Input", "5V/4A barrel or MicroUSB", "USB-C (Dev Kit PSU)", "USB-C (Dev Kit PSU)", "Included PSU", "5V/3A USB-C", "USB bus power", "5V/5A USB-C", "5V/~300mA"],
    ["Typical Power", "5-10W", "7-15W", "7-25W", "15-60W", "2-3W", "~0.5W (TPU only)", "5-12W", "1-2W"],
    ["Dimensions", "100x80mm (module)", "100x79mm (module)", "Dev Kit ~130x120mm", "Dev Kit ~110x110mm", "88x60mm", "USB dongle", "85x56mm", "40x27mm"],
    ["Cooling", "Passive heatsink/fan", "Dev Kit heatsink+fan", "Dev Kit heatsink+fan", "Active fan (included)", "Passive", "Passive", "Optional fan HAT", "Passive"]
]
for i, row_data in enumerate(ws7_data):
    r = 5 + i
    for j, val in enumerate(row_data):
        ws7.cell(row=r, column=j+1, value=val)
    format_data_row(ws7, r, 1, len(ws7_headers), is_alt=(i%2==1))

cols_w7 = {get_column_letter(i+1): 20 for i in range(len(ws7_headers))}
cols_w7['A'] = 25
adjust_col_widths(ws7, cols_w7)


# --- SHEET 8: Software & Platform Compatibility ---
ws8 = wb.create_sheet("8. Software Compatibility")
apply_base_formatting(ws8, "SOFTWARE & PLATFORM COMPATIBILITY", "Operating Systems, Frameworks, and Tools")
ws8.freeze_panes = "B5"

for i, h in enumerate(ws7_headers): # Reuse same headers mostly
    val = "Software/Platform" if i == 0 else h
    ws8.cell(row=4, column=i+1, value=val)
format_header_row(ws8, 4, 1, len(ws7_headers))

ws8_data = [
    ["Ubuntu", "18.04 (JetPack 4.x)", "22.04 (JetPack 6.x)", "22.04 (JetPack 6.x)", "22.04 (JetPack 6.x)", "Mendel Linux (Debian)", "Host dependent", "22.04/24.04", "No"],
    ["Linux", "Yes", "Yes", "Yes", "Yes", "Yes (Mendel)", "Host dependent", "Yes", "FreeRTOS/Arduino"],
    ["Python", "3.6 (older)", "3.10+", "3.10+", "3.10+", "3.7", "Host dependent", "3.11+", "MicroPython (limited)"],
    ["PyTorch", "Yes (1.x only)", "Yes (2.x native)", "Yes (2.x native)", "Yes (2.x native)", "No", "No", "Yes (CPU only)", "No"],
    ["TorchVision", "Yes (older)", "Yes (native)", "Yes (native)", "Yes (native)", "No", "No", "Yes (CPU only)", "No"],
    ["TensorFlow", "Yes (older)", "Yes", "Yes", "Yes", "Yes (for conversion)", "Yes (for conversion)", "Yes (CPU)", "No"],
    ["TensorRT", "Yes (7.x)", "Yes (8.x+)", "Yes (8.x+)", "Yes (8.x+)", "No", "No", "No", "No"],
    ["ONNX Runtime", "Yes", "Yes", "Yes", "Yes", "Partial", "Partial", "Yes", "No"],
    ["OpenCV", "Yes", "Yes", "Yes", "Yes", "Yes", "Via host", "Yes", "Limited (no pip)"],
    ["CUDA", "Yes (10.2)", "Yes (12.x)", "Yes (12.x)", "Yes (12.x)", "No", "No", "No", "No"],
    ["cuDNN", "Yes (8.x)", "Yes (8.x+)", "Yes (8.x+)", "Yes (8.x+)", "No", "No", "No", "No"],
    ["TFLite", "Yes", "Yes", "Yes", "Yes", "Yes (required)", "Yes (required)", "Yes", "TFLite Micro (very limited)"],
    ["Edge TPU Runtime", "No", "No", "No", "No", "Yes", "Yes", "Yes (with USB Coral)", "No"],
    ["Docker", "Yes", "Yes", "Yes", "Yes", "Limited", "Via host", "Yes", "No"],
    ["Jupyter Notebook", "Yes", "Yes", "Yes", "Yes", "Yes", "Via host", "Yes", "No"],
    ["VS Code (Remote)", "Yes", "Yes", "Yes", "Yes", "Yes", "Via host", "Yes", "PlatformIO"]
]
for i, row_data in enumerate(ws8_data):
    r = 5 + i
    for j, val in enumerate(row_data):
        ws8.cell(row=r, column=j+1, value=val)
    format_data_row(ws8, r, 1, len(ws7_headers), is_alt=(i%2==1))

notes_text = """Key Limitations:
- Jetson Nano is limited to JetPack 4.x (Ubuntu 18.04, CUDA 10.2, older PyTorch). Not recommended for new projects.
- Coral devices require model conversion to TFLite + Edge TPU compilation. Cannot run PyTorch directly.
- Raspberry Pi 5 can run PyTorch but CPU-only — no GPU acceleration. Inference will be slower.
- ESP32-CAM cannot run any standard ML framework. Only suitable as IoT image capture device."""
ws8.merge_cells('A22:I26')
cell = ws8.cell(row=22, column=1)
cell.value = notes_text
cell.font = data_font
cell.alignment = align_left
cell.border = thin_border
cell.fill = white_fill
adjust_col_widths(ws8, cols_w7)


# --- SHEET 9: ML Model Deployment ---
ws9 = wb.create_sheet("9. ML Model Deployment")
apply_base_formatting(ws9, "ML MODEL DEPLOYMENT COMPATIBILITY", "Loading and Running MobileNetV3 Large")
ws9.freeze_panes = "B5"

for i, h in enumerate(ws7_headers): 
    val = "Question" if i == 0 else h
    ws9.cell(row=4, column=i+1, value=val)
format_header_row(ws9, 4, 1, len(ws7_headers))

ws9_data = [
    ["Can run best_model.pth directly?", "Yes (with older PyTorch)", "Yes", "Yes", "Yes", "No", "No", "Yes (CPU only)", "No"],
    ["PyTorch native support?", "Yes (v1.x)", "Yes (v2.x)", "Yes (v2.x)", "Yes (v2.x)", "No", "No", "Yes (CPU)", "No"],
    ["CUDA acceleration?", "Yes (CUDA 10.2)", "Yes (CUDA 12.x)", "Yes (CUDA 12.x)", "Yes (CUDA 12.x)", "No", "No", "No", "No"],
    ["TensorRT optimization?", "Yes (TRT 7.x)", "Yes (TRT 8.x+)", "Yes (TRT 8.x+)", "Yes (TRT 8.x+)", "No", "No", "No", "No"],
    ["ONNX conversion recommended?", "Optional", "Recommended for TRT", "Recommended for TRT", "Recommended for TRT", "Required", "Required", "Optional", "N/A"],
    ["TFLite conversion required?", "No", "No", "No", "No", "Yes (mandatory)", "Yes (mandatory)", "Optional", "N/A"],
    ["INT8 quantization supported?", "Limited", "Yes", "Yes", "Yes", "Yes (required for TPU)", "Yes (required for TPU)", "No", "N/A"],
    ["FP16 inference?", "Yes", "Yes", "Yes", "Yes", "No (INT8 only on TPU)", "No (INT8 only on TPU)", "No", "N/A"],
    ["Model conversion complexity", "None", "None (optional TRT)", "None (optional TRT)", "None (optional TRT)", "High (multi-step)", "High (multi-step)", "None", "Not feasible"],
    ["Deployment difficulty", "Medium", "Easy", "Easy", "Easy", "Hard", "Hard", "Easy", "Not feasible"],
    ["Expected inference speed", "Medium", "High", "Very High", "Very High", "Medium (TPU)", "Medium (TPU)", "Low (CPU only)", "Not feasible"],
    ["Power efficiency for inference", "Good (5-10W)", "Very Good (7-15W)", "Good (7-25W)", "Low (15-60W)", "Excellent (2-3W)", "Excellent (0.5W TPU)", "Good (5-12W)", "N/A"]
]
for i, row_data in enumerate(ws9_data):
    r = 5 + i
    for j, val in enumerate(row_data):
        ws9.cell(row=r, column=j+1, value=val)
    format_data_row(ws9, r, 1, len(ws7_headers), is_alt=(i%2==1))

format_section_header(ws9, 19, "RECOMMENDED DEPLOYMENT PIPELINES", 1, 9)
pipelines = """For Jetson Orin Nano / Super / AGX Orin:
  Pipeline A (Direct): best_model.pth -> PyTorch -> model.eval() -> torch.no_grad() -> inference
  Pipeline B (Optimized): best_model.pth -> torch.onnx.export() -> .onnx -> trtexec -> .engine -> TensorRT inference

For Jetson Nano:
  Pipeline: best_model.pth -> PyTorch 1.x -> model.eval() -> inference (limited by old software)

For Coral Dev Board / USB:
  Pipeline: best_model.pth -> torch.onnx.export() -> .onnx -> onnx-tf -> SavedModel -> tflite_convert -> .tflite -> edgetpu_compiler -> _edgetpu.tflite
  Note: Complex multi-step process. May fail if model uses unsupported operations.

For Raspberry Pi 5:
  Pipeline A: best_model.pth -> PyTorch CPU -> inference (slow but works)
  Pipeline B: best_model.pth -> ONNX -> ONNX Runtime CPU -> inference (faster)

For ESP32-CAM:
  Not feasible. MobileNetV3 Large requires ~12MB+ model size and significant compute. ESP32 has 520KB SRAM."""
ws9.merge_cells('A20:I35')
cell = ws9.cell(row=20, column=1)
cell.value = pipelines
cell.font = data_font
cell.alignment = align_left
cell.border = thin_border
cell.fill = white_fill
adjust_col_widths(ws9, cols_w7)


# --- SHEET 10: Performance & AI Capability ---
ws10 = wb.create_sheet("10. Performance & AI")
apply_base_formatting(ws10, "PERFORMANCE & AI CAPABILITY", "Compute Power and Inference Speed")
ws10.freeze_panes = "B5"

for i, h in enumerate(ws7_headers): 
    val = "Metric" if i == 0 else h
    ws10.cell(row=4, column=i+1, value=val)
format_header_row(ws10, 4, 1, len(ws7_headers))

ws10_data = [
    ["AI Performance (TOPS/GFLOPS)", "472 GFLOPS (FP16)", "40 TOPS (INT8)", "67 TOPS (INT8)", "275 TOPS (INT8)", "4 TOPS (INT8)", "4 TOPS (INT8)", "~30 GFLOPS (est.)", "Negligible"],
    ["CUDA Cores", "128", "1024", "1024", "2048", "0", "0", "0", "0"],
    ["Tensor Cores", "0", "32", "32", "64", "0", "0", "0", "0"],
    ["FP32 Capability", "Yes", "Yes", "Yes", "Yes", "No", "No", "Limited (CPU)", "No"],
    ["FP16 Capability", "Yes", "Yes", "Yes", "Yes", "No", "No", "No", "No"],
    ["INT8 Capability", "Limited", "Yes", "Yes", "Yes", "Yes (Edge TPU)", "Yes (Edge TPU)", "No", "No"],
    ["Memory Bandwidth", "25.6 GB/s", "68 GB/s", "68 GB/s", "204.8 GB/s", "14.9 GB/s", "N/A", "~32 GB/s", "N/A"],
    ["RAM Available", "4GB", "8GB", "8GB", "32GB", "4GB", "Host RAM", "4/8GB", "4MB PSRAM"],
    ["Suitability for MobileNetV3 Large", "Adequate", "Excellent", "Excellent", "Excellent", "Good (after conversion)", "Good (after conversion)", "Adequate (CPU)", "Not suitable"],
    ["Real-Time Inference (est.)", "Yes (~15-30 FPS)", "Yes (~60+ FPS)", "Yes (~100+ FPS)", "Yes (~200+ FPS)", "Yes (~30 FPS, TPU)", "Yes (~30 FPS, TPU)", "Marginal (~5-10 FPS)", "No"],
    ["Multi-Camera Support", "Limited (1-2)", "Yes (2-4)", "Yes (2-4)", "Yes (6+)", "Limited (1)", "1 (via host)", "Limited (1-2)", "1 (built-in)"],
    ["Future Model Scalability", "Low", "High", "High", "Very High", "Low", "Low", "Medium", "None"]
]
for i, row_data in enumerate(ws10_data):
    r = 5 + i
    for j, val in enumerate(row_data):
        ws10.cell(row=r, column=j+1, value=val)
    format_data_row(ws10, r, 1, len(ws7_headers), is_alt=(i%2==1))

ws10.cell(row=18, column=1, value="Note: FPS estimates are approximate and depend on optimization, model precision, and system configuration. Actual benchmarks should be performed on the target device.")
ws10.merge_cells('A18:I18')
ws10.cell(row=18, column=1).font = Font(name='Calibri', size=9, italic=True)
adjust_col_widths(ws10, cols_w7)


# --- SHEET 11: Power & Deployment ---
ws11 = wb.create_sheet("11. Power & Deployment")
apply_base_formatting(ws11, "POWER & DEPLOYMENT CONSIDERATIONS", "Practicalities of Real-World Deployment")
ws11.freeze_panes = "B5"

for i, h in enumerate(ws7_headers): 
    val = "Consideration" if i == 0 else h
    ws11.cell(row=4, column=i+1, value=val)
format_header_row(ws11, 4, 1, len(ws7_headers))

ws11_data = [
    ["Typical Power Draw", "5-10W", "7-15W", "7-25W", "15-60W", "2-3W", "~0.5W", "5-12W", "1-2W"],
    ["Power Supply", "5V/4A barrel", "Dev Kit PSU (19V)", "Dev Kit PSU (19V)", "Included PSU", "5V/3A USB-C", "USB bus power", "5V/5A USB-C", "5V USB"],
    ["Cooling Required", "Passive/optional fan", "Heatsink + fan (included)", "Heatsink + fan (included)", "Active fan (included)", "Passive", "Passive", "Optional fan HAT", "Passive"],
    ["Battery Operation", "Possible (5V powerbank)", "Difficult (higher power)", "Difficult (higher power)", "Not practical", "Yes (powerbank)", "Yes (USB powered)", "Possible (powerbank)", "Yes (small battery)"],
    ["Lab/Demo Suitability", "Good", "Excellent", "Excellent", "Good (bulky)", "Good", "Good (with host)", "Excellent", "Limited (no ML)"],
    ["Field Prototype", "Possible", "Good", "Good", "Difficult (power/size)", "Good (low power)", "Good (with RPi)", "Good", "Excellent (IoT only)"],
    ["Agricultural Deployment", "Limited (EOL)", "Suitable", "Suitable", "Overkill", "Limited (EOL)", "Limited (EOL)", "Suitable", "IoT sensor only"],
    ["Outdoor Considerations", "Needs enclosure, no Wi-Fi", "Needs enclosure, add Wi-Fi", "Needs enclosure, add Wi-Fi", "Needs enclosure, high power", "Has Wi-Fi, low power", "Via host", "Has Wi-Fi, moderate", "Built-in Wi-Fi, rugged"],
    ["Portability", "Moderate", "Moderate", "Moderate", "Low (larger, heavier)", "Good (small, light)", "Excellent (tiny)", "Good (small)", "Excellent (very small)"],
    ["Setup Complexity", "Medium", "Easy (JetPack)", "Easy (JetPack)", "Easy (JetPack)", "Medium (Mendel)", "Medium (driver install)", "Easy (RPi OS)", "Easy (Arduino IDE)"],
    ["Maintenance", "Low (but EOL)", "Low", "Low", "Low", "Low (but EOL)", "Low (but EOL)", "Low", "Low"],
    ["Recommended Deployment", "Not recommended", "College demo + prototype", "College demo + prototype", "Research lab", "Not recommended (EOL)", "Budget add-on (EOL risk)", "Budget demo", "IoT sensor node"]
]
for i, row_data in enumerate(ws11_data):
    r = 5 + i
    for j, val in enumerate(row_data):
        ws11.cell(row=r, column=j+1, value=val)
    format_data_row(ws11, r, 1, len(ws7_headers), is_alt=(i%2==1))
adjust_col_widths(ws11, cols_w7)


# --- SHEET 12: Device Analysis ---
ws12 = wb.create_sheet("12. Device Analysis")
apply_base_formatting(ws12, "DEVICE-BY-DEVICE ANALYSIS", "In-Depth Strengths and Weaknesses")
ws12.freeze_panes = "B5"

for i, h in enumerate(ws7_headers): 
    val = "Analysis Question" if i == 0 else h
    ws12.cell(row=4, column=i+1, value=val)
format_header_row(ws12, 4, 1, len(ws7_headers))

ws12_data = [
    ["What is it?", "Entry-level NVIDIA edge AI SBC (discontinued)", "Mid-range NVIDIA Orin edge AI SBC", "Enhanced Orin Nano with unlocked 67 TOPS", "High-end NVIDIA edge AI platform", "Google's Edge TPU development board", "USB AI accelerator dongle for Edge TPU", "Popular general-purpose SBC", "Ultra-low-cost IoT camera module"],
    ["Key Specs", "A57 CPU, 128 CUDA, 4GB", "A78AE CPU, 1024 CUDA, 40 TOPS, 8GB", "A78AE CPU, 1024 CUDA, 67 TOPS, 8GB", "A78AE 12-core, 2048 CUDA, 275 TOPS, 32GB", "A53 CPU, Edge TPU 4 TOPS, 4GB", "Edge TPU 4 TOPS only", "A76 CPU, VideoCore VII, 4/8GB", "Xtensa 240MHz, 520KB+4MB"],
    ["AI Capability", "Basic GPU ML inference", "Strong edge AI", "Very strong edge AI", "Top-tier edge AI", "Edge TPU inference (INT8 only)", "Edge TPU inference (INT8 only)", "CPU-only ML inference", "Cannot run ML models"],
    ["Framework Support", "PyTorch 1.x, TF, TRT 7", "PyTorch 2.x, TF, TRT 8+, ONNX", "PyTorch 2.x, TF, TRT 8+, ONNX", "PyTorch 2.x, TF, TRT 8+, ONNX", "TFLite + Edge TPU only", "TFLite + Edge TPU only", "PyTorch (CPU), TF (CPU), ONNX", "Arduino/MicroPython only"],
    ["Can run MobileNetV3 .pth?", "Yes (with older PyTorch)", "Yes (natively)", "Yes (natively)", "Yes (natively)", "No (needs TFLite conversion)", "No (needs TFLite conversion)", "Yes (CPU only, slow)", "No"],
    ["Model Conversion Needed?", "No", "No (optional TRT)", "No (optional TRT)", "No (optional TRT)", "Yes (complex multi-step)", "Yes (complex multi-step)", "No", "Not feasible"],
    ["Camera Support", "CSI + USB", "CSI + USB", "CSI + USB", "CSI + USB", "CSI + USB", "Via host device", "CSI + USB", "Built-in OV2640 (2MP)"],
    ["Connectivity", "USB, Ethernet, GPIO", "USB 3.2, GbE, GPIO", "USB 3.2, GbE, GPIO", "USB 3.2, 10GbE, GPIO", "USB, Wi-Fi, BT, Ethernet", "USB only", "USB, Wi-Fi, BT, GbE", "Wi-Fi, BT, GPIO"],
    ["Strengths", "CUDA GPU, good docs, cheap if available", "Excellent AI perf, native PyTorch, modern", "Best TOPS/dollar, same HW upgradeable", "Most powerful, 32GB RAM, multi-model", "Low power, built-in Wi-Fi", "Cheapest AI accelerator, portable", "Affordable, huge community, versatile", "Ultra-cheap, Wi-Fi, built-in camera"],
    ["Weaknesses", "EOL, old software, no Wi-Fi", "No built-in Wi-Fi, India price varies", "No built-in Wi-Fi, India price varies", "Very expensive, high power, overkill", "EOL, needs model conversion, no PyTorch", "EOL, needs host, needs conversion", "No GPU acceleration, slow inference", "Cannot run any real ML model"],
    ["Est. Total Project Cost", "INR 18,000-25,000", "INR 36,000-81,000", "INR 36,000-81,000", "INR 2,04,000-3,04,000", "INR 21,000-24,500", "INR 25,000-33,500 (with RPi5)", "INR 18,000-19,000", "INR 700-1,300"],
    ["Deployment Difficulty", "Medium", "Easy", "Easy", "Easy", "Hard", "Hard", "Easy", "Not feasible for ML"],
    ["Suitability for Project", "Not recommended (EOL)", "Highly suitable", "Highly suitable (best value)", "Suitable but overkill/expensive", "Possible but risky (EOL)", "Possible but risky (EOL)", "Budget option (slower)", "IoT capture device only"],
    ["Real-Time Capable?", "Yes (moderate speed)", "Yes (fast)", "Yes (very fast)", "Yes (extremely fast)", "Yes (after conversion)", "Yes (after conversion)", "Marginal (CPU bottleneck)", "No"],
    ["IoT Integration", "Limited (no Wi-Fi)", "Add Wi-Fi module", "Add Wi-Fi module", "Add Wi-Fi module", "Built-in Wi-Fi", "Via host", "Built-in Wi-Fi", "Excellent (native IoT)"],
    ["Power Efficiency", "Good", "Very Good", "Good", "Poor (high power)", "Excellent", "Excellent", "Good", "Excellent"],
    ["Recommended For", "Legacy/existing hardware", "Best overall choice", "Best overall choice", "Research/multi-model", "Not recommended", "Budget AI add-on", "Budget projects", "Image capture IoT node"],
    ["Final Verdict", "Not Recommended", "Highly Recommended", "Highly Recommended", "Recommended (if budget allows)", "Possible (proceed with caution)", "Possible (proceed with caution)", "Recommended (budget)", "Not Recommended (for ML)"]
]
for i, row_data in enumerate(ws12_data):
    r = 5 + i
    for j, val in enumerate(row_data):
        ws12.cell(row=r, column=j+1, value=val)
    format_data_row(ws12, r, 1, len(ws7_headers), is_alt=(i%2==1))
adjust_col_widths(ws12, cols_w7)


# --- SHEET 13: Decision Matrix ---
ws13 = wb.create_sheet("13. Decision Matrix")
apply_base_formatting(ws13, "HARDWARE DECISION MATRIX", "Quantitative Evaluation and Ranking")

ws13.cell(row=4, column=1, value="Weights").font = header_font
ws13.cell(row=4, column=1).fill = header_fill
ws13.cell(row=4, column=2, value="Weight (%)").font = header_font
ws13.cell(row=4, column=2).fill = header_fill

weights = {
    "ML/AI Performance": 20,
    "PyTorch Compatibility": 15,
    "Ease of Deployment": 15,
    "Price (inverse: lower=better)": 15,
    "Power Efficiency": 10,
    "Camera Integration": 10,
    "IoT Connectivity": 5,
    "Future Scalability": 10
}
row = 5
for k, v in weights.items():
    ws13.cell(row=row, column=1, value=k).border = thin_border
    ws13.cell(row=row, column=2, value=v).border = thin_border
    row += 1
ws13.cell(row=row, column=1, value="Total").font = Font(bold=True)
ws13.cell(row=row, column=2, value=f"=SUM(B5:B{row-1})").font = Font(bold=True)
ws13.cell(row=row, column=1).border = thin_border
ws13.cell(row=row, column=2).border = thin_border


format_section_header(ws13, 14, "RAW SCORES (Out of 10)", 1, 10)
raw_headers = ["Device", "ML/AI Perf", "PyTorch", "Ease Deploy", "Price", "Power", "Camera", "IoT", "Scalability"]
for i, h in enumerate(raw_headers):
    ws13.cell(row=15, column=i+1, value=h)
format_header_row(ws13, 15, 1, len(raw_headers))

raw_scores = [
    ["Jetson Nano", 4, 5, 6, 7, 7, 8, 3, 2],
    ["Jetson Orin Nano", 8, 10, 9, 6, 8, 9, 4, 9],
    ["Jetson Orin Nano Super", 9, 10, 9, 6, 7, 9, 4, 9],
    ["Jetson AGX Orin", 10, 10, 8, 2, 4, 10, 4, 10],
    ["Coral Dev Board", 5, 2, 4, 6, 9, 7, 6, 3],
    ["Coral USB Acc.", 5, 2, 4, 7, 10, 6, 5, 3],
    ["Raspberry Pi 5", 3, 6, 9, 9, 8, 8, 8, 6],
    ["ESP32-CAM", 0, 0, 1, 10, 10, 4, 9, 1]
]
for i, r_data in enumerate(raw_scores):
    r = 16 + i
    for j, val in enumerate(r_data):
        ws13.cell(row=r, column=j+1, value=val)
    format_data_row(ws13, r, 1, len(raw_headers), is_alt=(i%2==1))


format_section_header(ws13, 26, "WEIGHTED SCORES & FINAL RECOMMENDATION", 1, 11)
weighted_headers = raw_headers + ["Total", "Recommendation"]
for i, h in enumerate(weighted_headers):
    ws13.cell(row=27, column=i+1, value=h)
format_header_row(ws13, 27, 1, len(weighted_headers))

for i, r_data in enumerate(raw_scores):
    r = 28 + i
    ws13.cell(row=r, column=1, value=r_data[0]) # Device
    ws13.cell(row=r, column=2, value=f"=B{16+i}*$B$5/10")
    ws13.cell(row=r, column=3, value=f"=C{16+i}*$B$6/10")
    ws13.cell(row=r, column=4, value=f"=D{16+i}*$B$7/10")
    ws13.cell(row=r, column=5, value=f"=E{16+i}*$B$8/10")
    ws13.cell(row=r, column=6, value=f"=F{16+i}*$B$9/10")
    ws13.cell(row=r, column=7, value=f"=G{16+i}*$B$10/10")
    ws13.cell(row=r, column=8, value=f"=H{16+i}*$B$11/10")
    ws13.cell(row=r, column=9, value=f"=I{16+i}*$B$12/10")
    
    ws13.cell(row=r, column=10, value=f"=SUM(B{r}:I{r})") # Total
    ws13.cell(row=r, column=11, value=f'=IF(J{r}>=80,"Highly Recommended",IF(J{r}>=60,"Recommended",IF(J{r}>=40,"Possible","Not Recommended")))')
    
    format_data_row(ws13, r, 1, 11, is_alt=(i%2==1))
    ws13.cell(row=r, column=10).number_format = '0.0'

# Conditional Formatting for Total column
rule_db = DataBarRule(start_type='min', end_type='max', color='2E5FA1')
ws13.conditional_formatting.add('J28:J35', rule_db)

# Conditional Formatting for Recommendation column
rule_highly = CellIsRule(operator='equal', formula=['"Highly Recommended"'], fill=green_fill)
rule_rec = CellIsRule(operator='equal', formula=['"Recommended"'], fill=rec_blue_fill)
rule_pos = CellIsRule(operator='equal', formula=['"Possible"'], fill=yellow_fill)
rule_not = CellIsRule(operator='equal', formula=['"Not Recommended"'], fill=red_fill)
ws13.conditional_formatting.add('K28:K35', rule_highly)
ws13.conditional_formatting.add('K28:K35', rule_rec)
ws13.conditional_formatting.add('K28:K35', rule_pos)
ws13.conditional_formatting.add('K28:K35', rule_not)


format_section_header(ws13, 37, "RANKING", 1, 4)
rank_headers = ["Rank", "Device", "Total Score", "Recommendation"]
for i, h in enumerate(rank_headers):
    ws13.cell(row=38, column=i+1, value=h)
format_header_row(ws13, 38, 1, 4)

for i in range(8):
    r = 39 + i
    r_src = 28 + i
    ws13.cell(row=r, column=1, value=f"=RANK(J{r_src},$J$28:$J$35)")
    ws13.cell(row=r, column=2, value=f"=A{r_src}")
    ws13.cell(row=r, column=3, value=f"=J{r_src}")
    ws13.cell(row=r, column=4, value=f"=K{r_src}")
    format_data_row(ws13, r, 1, 4, is_alt=(i%2==1))

ws13.conditional_formatting.add('D39:D46', rule_highly)
ws13.conditional_formatting.add('D39:D46', rule_rec)
ws13.conditional_formatting.add('D39:D46', rule_pos)
ws13.conditional_formatting.add('D39:D46', rule_not)

adjust_col_widths(ws13, {'A':25, 'B':15, 'C':15, 'D':15, 'E':15, 'F':15, 'G':15, 'H':15, 'I':15, 'J':15, 'K':25})


# --- SHEET 14: Final Recommendation ---
ws14 = wb.create_sheet("14. Final Recommendation")
apply_base_formatting(ws14, "FINAL RECOMMENDATIONS", "Tailored Solutions for Project Success")

format_section_header(ws14, 4, "RECOMMENDATION BY SCENARIO", 1, 4)
ws14_h1 = ["Scenario", "Recommended Device", "Score", "Why"]
for i, h in enumerate(ws14_h1):
    ws14.cell(row=5, column=i+1, value=h)
format_header_row(ws14, 5, 1, 4)

scenario_data = [
    ["A. Best for college demo", "Jetson Orin Nano Super", "92/100", "Native PyTorch, fast inference, $249, modern software"],
    ["B. Best budget", "Raspberry Pi 5 (8GB)", "68/100", "Affordable INR 18-19K total, PyTorch works (CPU), large community"],
    ["C. Best for real-time inference", "Jetson Orin Nano Super", "92/100", "67 TOPS, TensorRT, CUDA 12.x, estimated 100+ FPS"],
    ["D. Best for IoT integration", "RPi 5 + ESP32 sensors", "68/100", "Built-in Wi-Fi, GPIO, MQTT support, easy sensor integration"],
    ["E. Best for field deployment", "Jetson Orin Nano + Wi-Fi module", "80/100", "Moderate power, compact, reliable AI inference"],
    ["F. Best high-performance", "Jetson AGX Orin", "85/100", "275 TOPS, 32GB RAM, multi-model, but expensive"]
]
for i, row_data in enumerate(scenario_data):
    r = 6 + i
    for j, val in enumerate(row_data):
        ws14.cell(row=r, column=j+1, value=val)
    format_data_row(ws14, r, 1, 4, is_alt=(i%2==1))


format_section_header(ws14, 14, "MY FINAL RECOMMENDATION", 1, 2)
ws14_h2 = ["Category", "Recommendation"]
for i, h in enumerate(ws14_h2):
    ws14.cell(row=15, column=i+1, value=h)
format_header_row(ws14, 15, 1, 2)

final_data = [
    ["Recommended Edge AI Device", "NVIDIA Jetson Orin Nano Super Developer Kit"],
    ["Recommended Camera", "Raspberry Pi Camera Module 3 (CSI) or Logitech USB webcam"],
    ["Optional IoT Device", "ESP32 modules for sensors + Wi-Fi data transmission"],
    ["Recommended Deployment Framework", "PyTorch (direct) or TensorRT (optimized)"],
    ["Recommended Model Format", ".pth (PyTorch native) -> optional .onnx -> .engine (TensorRT)"],
    ["Estimated Total Budget", "INR 36,000 - 81,000 (varies by seller)"],
    ["Deployment Difficulty", "Easy (JetPack SDK provides everything)"],
    ["Expected Inference Speed", "High (real-time with TensorRT optimization)"]
]
for i, row_data in enumerate(final_data):
    r = 16 + i
    for j, val in enumerate(row_data):
        ws14.cell(row=r, column=j+1, value=val)
    format_data_row(ws14, r, 1, 2, is_alt=(i%2==1))
    ws14.cell(row=r, column=1).font = Font(bold=True)


format_section_header(ws14, 26, "WHY JETSON ORIN NANO SUPER IS THE BEST CHOICE", 1, 4)
reasons = [
    "1. Native PyTorch 2.x support — your best_model.pth works directly without any conversion",
    "2. 67 TOPS AI performance — massive improvement over alternatives",
    "3. CUDA 12.x + TensorRT 8.x+ — GPU-accelerated inference with optimization path",
    "4. $249 MSRP — best performance-per-dollar in the Jetson lineup",
    "5. 8GB LPDDR5 RAM — plenty for MobileNetV3 Large + preprocessing",
    "6. JetPack 6.x SDK — modern, well-documented, actively supported",
    "7. NVMe SSD support — fast storage for OS and model files",
    "8. CSI + USB camera support — flexible camera options",
    "9. Same hardware as Orin Nano — can upgrade existing units via software",
    "10. Future scalability — can run larger models, multi-camera, TensorRT"
]
for i, reason in enumerate(reasons):
    r = 27 + i
    ws14.cell(row=r, column=1, value=reason)
    ws14.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    format_data_row(ws14, r, 1, 4, is_alt=(i%2==1))


format_section_header(ws14, 39, "WHY NOT THE ALTERNATIVES?", 1, 2)
ws14.cell(row=40, column=1, value="Device").font = header_font
ws14.cell(row=40, column=1).fill = header_fill
ws14.cell(row=40, column=2, value="Reason Not Primary Choice").font = header_font
ws14.cell(row=40, column=2).fill = header_fill

alt_reasons = [
    ["Jetson Nano", "End-of-Life, stuck on old JetPack 4.x / CUDA 10.2, no future support"],
    ["Jetson AGX Orin", "8x more expensive ($1999 vs $249), massively overkill for single MobileNetV3 model"],
    ["Coral Dev Board", "End-of-Life, requires complex model conversion to TFLite+Edge TPU, no PyTorch"],
    ["Coral USB", "End-of-Life, requires host device, same conversion issues as Coral Dev Board"],
    ["Raspberry Pi 5", "No GPU acceleration, CPU-only PyTorch is significantly slower, adequate for budget demos only"],
    ["ESP32-CAM", "Cannot run MobileNetV3 Large (520KB SRAM vs ~12MB+ model), useful only as IoT capture device"]
]
for i, row_data in enumerate(alt_reasons):
    r = 41 + i
    for j, val in enumerate(row_data):
        ws14.cell(row=r, column=j+1, value=val)
    format_data_row(ws14, r, 1, 2, is_alt=(i%2==1))
    ws14.cell(row=r, column=1).font = Font(bold=True)

adjust_col_widths(ws14, {'A':35, 'B':40, 'C':15, 'D':50})


# --- SHEET 15: Sources & References ---
ws15 = wb.create_sheet("15. Sources & References")
apply_base_formatting(ws15, "SOURCES & REFERENCES", "Data Origins and Additional Reading")
ws15.freeze_panes = "A5"

ws15_headers = ["S.No.", "Source", "Device/Topic", "Information Used", "URL", "Access Date", "Source Type"]
for i, h in enumerate(ws15_headers):
    ws15.cell(row=4, column=i+1, value=h)
format_header_row(ws15, 4, 1, len(ws15_headers))

sources_data = [
    [1, "NVIDIA", "Jetson Orin Nano", "Specifications, pricing", "https://developer.nvidia.com/embedded/jetson-orin-nano", "Jul 2026", "Official"],
    [2, "NVIDIA", "Jetson AGX Orin", "Specifications, pricing", "https://developer.nvidia.com/embedded/jetson-agx-orin", "Jul 2026", "Official"],
    [3, "NVIDIA", "Jetson Nano", "EOL status, specifications", "https://developer.nvidia.com/embedded/jetson-nano", "Jul 2026", "Official"],
    [4, "NVIDIA", "JetPack SDK", "Software compatibility", "https://developer.nvidia.com/embedded/jetpack", "Jul 2026", "Official"],
    [5, "NVIDIA", "TensorRT", "Optimization framework", "https://developer.nvidia.com/tensorrt", "Jul 2026", "Official"],
    [6, "Google", "Coral Dev Board", "Specifications", "https://coral.ai/products/dev-board", "Jul 2026", "Official"],
    [7, "Google", "Coral USB Accelerator", "Specifications", "https://coral.ai/products/accelerator", "Jul 2026", "Official"],
    [8, "Google", "Edge TPU", "AI accelerator details", "https://coral.ai/technology", "Jul 2026", "Official"],
    [9, "Raspberry Pi", "Raspberry Pi 5", "Specifications, pricing", "https://www.raspberrypi.com/products/raspberry-pi-5", "Jul 2026", "Official"],
    [10, "Espressif", "ESP32", "Specifications", "https://www.espressif.com/en/products/socs/esp32", "Jul 2026", "Official"],
    [11, "PyTorch", "PyTorch", "Framework documentation", "https://pytorch.org", "Jul 2026", "Official"],
    [12, "ONNX", "ONNX", "Model interchange format", "https://onnx.ai", "Jul 2026", "Official"],
    [13, "TensorFlow", "TFLite", "Edge deployment", "https://www.tensorflow.org/lite", "Jul 2026", "Official"],
    [14, "Robocraze", "Jetson India pricing", "India retail pricing", "https://robocraze.com", "Jul 2026", "Retailer"],
    [15, "ThinkRobotics", "Jetson AGX India", "India retail pricing", "https://thinkrobotics.com", "Jul 2026", "Retailer"],
    [16, "Robu.in", "RPi 5, ESP32 India", "India retail pricing", "https://robu.in", "Jul 2026", "Retailer"],
    [17, "IndiaMART", "Various devices", "India market pricing", "https://www.indiamart.com", "Jul 2026", "Marketplace"],
    [18, "OpenCV", "OpenCV", "Computer vision library", "https://opencv.org", "Jul 2026", "Official"],
    [19, "NVIDIA", "CUDA", "GPU computing platform", "https://developer.nvidia.com/cuda-zone", "Jul 2026", "Official"],
    [20, "MobileNetV3 Paper", "MobileNetV3", "Model architecture reference", "https://arxiv.org/abs/1905.02244", "Jul 2026", "Academic"]
]
for i, row_data in enumerate(sources_data):
    r = 5 + i
    for j, val in enumerate(row_data):
        cell = ws15.cell(row=r, column=j+1, value=val)
        if j == 4: # URL column
            cell.hyperlink = val
            cell.font = Font(name='Calibri', size=10, color="0563C1", underline="single")
    format_data_row(ws15, r, 1, len(ws15_headers), is_alt=(i%2==1))
    
adjust_col_widths(ws15, {'A':8, 'B':20, 'C':25, 'D':35, 'E':45, 'F':15, 'G':15})
ws15.auto_filter.ref = f"A4:G{len(sources_data)+4}"


# Save the workbook
wb.save("Plant_Disease_Edge_AI_IoT_Professional_Comparison.xlsx")
print("Excel workbook generated successfully at Plant_Disease_Edge_AI_IoT_Professional_Comparison.xlsx")
