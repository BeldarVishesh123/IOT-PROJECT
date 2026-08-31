import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule

def set_title(ws, title_text, end_col):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=end_col)
    cell = ws.cell(row=1, column=1)
    cell.value = title_text
    cell.font = Font(name='Calibri', size=16, bold=True, color='FFFFFF')
    cell.fill = PatternFill(start_color='002060', end_color='002060', fill_type='solid')
    cell.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 30
    
    # footer
    ws.cell(row=100, column=1).value = "Last Updated: July 2026"
    ws.cell(row=100, column=1).font = Font(name='Calibri', size=10, italic=True)

def format_table(ws, start_row, headers, data, apply_conditional_col=None):
    header_font = Font(name='Calibri', size=12, bold=True, color='FFFFFF')
    header_fill = PatternFill(start_color='004080', end_color='004080', fill_type='solid')
    data_font = Font(name='Calibri', size=11)
    wrap_alignment = Alignment(wrap_text=True, vertical='top')
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                         top=Side(style='thin'), bottom=Side(style='thin'))
    gray_fill = PatternFill(start_color='F2F2F2', end_color='F2F2F2', fill_type='solid')

    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=start_row, column=col_num)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    for row_num, row_data in enumerate(data, start_row + 1):
        is_even = (row_num % 2 == 0)
        for col_num, val in enumerate(row_data, 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.value = val
            cell.font = data_font
            cell.border = thin_border
            cell.alignment = wrap_alignment
            if is_even:
                cell.fill = gray_fill

    end_col_letter = get_column_letter(len(headers))
    ws.auto_filter.ref = f"A{start_row}:{end_col_letter}{start_row + len(data)}"

    for col_num in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col_num)].width = 25

    ws.freeze_panes = ws.cell(row=start_row + 1, column=1)

    if apply_conditional_col:
        green_fill = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
        blue_fill = PatternFill(start_color='B4C6E7', end_color='B4C6E7', fill_type='solid')
        yellow_fill = PatternFill(start_color='FFEB9C', end_color='FFEB9C', fill_type='solid')
        red_fill = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
        
        range_str = f"{apply_conditional_col}{start_row + 1}:{apply_conditional_col}{start_row + len(data)}"
        ws.conditional_formatting.add(range_str, CellIsRule(operator='equal', formula=['"Highly Recommended"'], fill=green_fill))
        ws.conditional_formatting.add(range_str, CellIsRule(operator='equal', formula=['"Recommended"'], fill=blue_fill))
        ws.conditional_formatting.add(range_str, CellIsRule(operator='equal', formula=['"Possible"'], fill=yellow_fill))
        ws.conditional_formatting.add(range_str, CellIsRule(operator='equal', formula=['"Not Recommended"'], fill=red_fill))

def main():
    wb = openpyxl.Workbook()
    
    # ---------------- SHEET 1 ----------------
    ws1 = wb.active
    ws1.title = "Executive Summary"
    set_title(ws1, "EXECUTIVE SUMMARY", 2)
    
    summary_data = [
        ["Project name", "Plant Disease Detection Using Edge AI and IoT"],
        ["Objective", "Deploy MobileNetV3 Large on edge device for real-time plant disease classification"],
        ["Model", "MobileNetV3 Large (PyTorch), ~97.19% accuracy, 15 classes"],
        ["Final recommended device", "NVIDIA Jetson Orin Nano Super Developer Kit"],
        ["Second-best", "Raspberry Pi 5 + Coral USB Accelerator"],
        ["Budget alternative", "Raspberry Pi 5 (CPU-only inference)"],
        ["NOT recommended", "ESP32-CAM (cannot run the model), Jetson Nano (EOL)"],
        ["Architecture diagram", "Plant Leaf -> Camera -> Edge Device (Jetson Orin Nano) -> MobileNetV3 Large -> Disease Prediction -> Confidence Score -> Optional: Wi-Fi -> Cloud/IoT Dashboard"],
        ["Key Takeaway", "NVIDIA Jetson Orin Nano Super Dev Kit provides the best balance of AI performance, PyTorch compatibility, and ease of deployment for the MobileNetV3 model."]
    ]
    
    format_table(ws1, 3, ["Item", "Description"], summary_data)
    ws1.column_dimensions['A'].width = 30
    ws1.column_dimensions['B'].width = 100

    # ---------------- SHEET 2 ----------------
    ws2 = wb.create_sheet("Device Comparison")
    set_title(ws2, "DEVICE COMPARISON", 57)
    
    headers2 = ["Device Name", "Manufacturer", "Device Category", "Edge/IoT/Both", "Release Year", "Availability Status", "Price India (INR)", "Price USD", "Price Notes", "CPU", "GPU", "GPU Architecture", "CUDA Cores", "Tensor Cores", "AI Accelerator/NPU/TPU", "AI Performance (TOPS)", "RAM", "Storage", "OS Support", "Linux", "Ubuntu", "Windows", "Python", "PyTorch", "TensorFlow", "TF Lite", "ONNX", "TensorRT", "Edge TPU", "OpenCV", "Camera Interface", "USB Camera", "CSI Camera", "Wi-Fi", "Bluetooth", "Ethernet", "USB Ports", "GPIO", "Power Requirements", "Power Consumption", "Cooling", "Form Factor", "Ease of Setup", "Ease of ML Deployment", "Model Conversion Required?", "Can Run .pth Directly?", "Recommended Framework", "Suitability for MobileNetV3", "Suitability for Plant Disease Detection", "Real-Time Inference", "Multi-Camera", "Future Expansion", "IoT Integration", "Main Advantages", "Main Disadvantages", "Overall Rating (/10)", "Recommendation"]
    
    data2 = [
        ["Google Coral Dev Board", "Google", "SBC", "Edge", "2019", "EOL", "17000-20500", "129.99", "Approx, EOL", "NXP i.MX 8M SoC (4x Cortex-A53 + Cortex-M4F)", "None", "None", "0", "0", "Google Edge TPU", "4 TOPS", "1GB/4GB LPDDR4", "8GB eMMC", "Linux (Mendel)", "Yes", "No", "No", "Yes", "No", "No", "Yes", "No", "No", "Yes", "Yes", "CSI, USB", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "5V/3A", "~2-3W", "Passive/Active", "Dev Board", "Medium", "Hard", "Yes", "No", "TF Lite", "Medium", "High", "Yes", "No", "Low", "Medium", "Edge TPU speed", "EOL, Conversion difficult", "5.5", "Possible"],
        ["Google Coral USB Accelerator", "Google", "AI Accelerator", "Edge", "2019", "EOL", "7500-16000", "59.99", "Approx, EOL", "None", "None", "None", "0", "0", "Google Edge TPU", "4 TOPS", "None", "None", "Linux/Mac/Win", "Yes", "Yes", "Yes", "Yes", "No", "No", "Yes", "No", "No", "Yes", "Yes", "USB (via host)", "Yes", "No", "No", "No", "No", "USB 3.0 Type-C", "No", "via USB", "~0.5W", "Passive", "USB Dongle", "Easy", "Hard", "Yes", "No", "TF Lite", "Medium", "High", "Yes", "No", "Low", "Low", "Cheap AI upgrade", "Requires host, EOL", "7.5", "Recommended"],
        ["NVIDIA Jetson Nano", "NVIDIA", "SBC", "Edge", "2019", "EOL", "Variable", "149", "Approx, EOL", "4x Cortex-A57", "Maxwell", "Maxwell", "128", "0", "None", "0.472 TFLOPS", "4GB LPDDR4", "MicroSD", "Ubuntu 18.04", "Yes", "Yes", "No", "Yes", "Older (1.x)", "Older", "Yes", "Yes", "Older", "No", "Yes", "CSI, USB", "Yes", "Yes", "No", "No", "Yes", "Yes", "Yes", "5V/4A or 5V/2A", "5-10W", "Passive", "Dev Board", "Medium", "Medium", "Yes", "Yes (slow)", "TensorRT", "Low", "Medium", "Partial", "Yes", "Low", "Medium", "CUDA support", "EOL, Old software", "4.0", "Not Recommended"],
        ["NVIDIA Jetson Orin Nano (8GB)", "NVIDIA", "SBC", "Edge", "2023", "Active", "30000-75000", "249", "Approx", "6x Cortex-A78AE", "Ampere", "Ampere", "1024", "32", "None", "40 TOPS", "8GB LPDDR5", "NVMe/MicroSD", "Ubuntu 22.04", "Yes", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No", "Yes", "CSI, USB", "Yes", "Yes", "No", "No", "Yes", "Yes", "Yes", "DC Jack", "7-15W", "Active", "Dev Board", "Easy", "Easy", "No/Optional", "Yes", "PyTorch/TensorRT", "High", "Very High", "Yes", "Yes", "High", "High", "Great performance", "Price varies in India", "9.0", "Highly Recommended"],
        ["NVIDIA Jetson Orin Nano Super Developer Kit", "NVIDIA", "SBC", "Edge", "2024", "Active", "30000-75000", "249", "Approx", "6x Cortex-A78AE", "Ampere", "Ampere", "1024", "32", "None", "67 TOPS", "8GB LPDDR5", "NVMe/MicroSD", "Ubuntu 22.04", "Yes", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No", "Yes", "CSI, USB", "Yes", "Yes", "No", "No", "Yes", "Yes", "Yes", "DC Jack", "7-15W", "Active", "Dev Board", "Easy", "Easy", "No/Optional", "Yes", "PyTorch/TensorRT", "Very High", "Very High", "Yes", "Yes", "Very High", "High", "Best value/perf", "Price varies in India", "9.5", "Highly Recommended"],
        ["NVIDIA Jetson AGX Orin", "NVIDIA", "SBC", "Edge", "2022", "Active", "200000-300000", "1999", "Approx", "12x Cortex-A78AE", "Ampere", "Ampere", "2048", "64", "None", "275 TOPS", "32GB LPDDR5", "64GB eMMC", "Ubuntu 22.04", "Yes", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No", "Yes", "CSI, USB", "Yes", "Yes", "No", "No", "10GbE", "Yes", "Yes", "DC Jack", "15-60W", "Active", "Dev Board", "Easy", "Easy", "No/Optional", "Yes", "PyTorch/TensorRT", "Overkill", "Overkill", "Yes", "Yes", "Very High", "High", "Massive performance", "Very expensive", "8.0", "Recommended"],
        ["Raspberry Pi 5", "Raspberry Pi", "SBC", "Edge/IoT", "2023", "Active", "5500-13000", "60-80", "Approx", "4x Cortex-A76", "VideoCore VII", "None", "0", "0", "None", "N/A", "4/8GB LPDDR4X", "MicroSD/NVMe", "RPi OS, Ubuntu", "Yes", "Yes", "No", "Yes", "Yes (CPU)", "Yes (CPU)", "Yes", "Yes", "No", "No", "Yes", "CSI, USB", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "5V/5A Type-C", "5-12W", "Active recommended", "Dev Board", "Easy", "Easy", "No", "Yes (CPU)", "ONNX/PyTorch", "Medium", "Medium", "Maybe (slower)", "No", "Medium", "Very High", "Cheap, community", "No AI acceleration", "7.0", "Recommended"],
        ["ESP32-CAM", "Espressif", "MCU", "IoT", "2018", "Active", "200-800", "5-10", "Approx", "2x Xtensa LX6", "None", "None", "0", "0", "None", "N/A", "520KB+4MB", "4MB Flash", "FreeRTOS", "No", "No", "No", "MicroPython", "No", "No", "Micro", "No", "No", "No", "No", "Built-in", "No", "No", "Yes", "Yes", "No", "No", "Yes", "5V", "~1-2W", "Passive", "Module", "Medium", "Not Feasible", "Yes", "No", "None", "Not Feasible", "Not Feasible", "No", "No", "Low", "High", "Ultra cheap", "Too weak for MobileNet", "2.0", "Not Recommended"]
    ]
    
    format_table(ws2, 3, headers2, data2, apply_conditional_col='BE') # column index 57 -> BE

    # ---------------- SHEET 3 ----------------
    ws3 = wb.create_sheet("Price Comparison")
    set_title(ws3, "PRICE COMPARISON", 13)
    
    headers3 = ["Device", "Base Price USD", "Base Price INR", "Camera Cost", "Power Supply Cost", "Storage Cost", "Cooling Cost", "Other Accessories", "Estimated Total Project Cost (INR)", "Price Source", "Price Date", "Price Reliability", "Notes"]
    data3 = [
        ["Google Coral Dev Board", "~$129.99", "17000-20500", "2000", "1000", "1000", "500", "1000", "20000-25000", "Various", "July 2026", "Low (EOL)", "EOL"],
        ["Coral USB + RPi 5", "~$140", "15000-24000", "2000", "1000", "1000", "500", "500", "20000-30000", "Various", "July 2026", "Medium", ""],
        ["NVIDIA Jetson Nano", "~$149", "13000+", "2000", "1000", "1000", "500", "500", "18000-25000", "Various", "July 2026", "Low (EOL)", "EOL"],
        ["NVIDIA Jetson Orin Nano", "~$249", "30000-75000", "2000", "1000", "2000", "Included", "500", "35000-85000", "Various", "July 2026", "High", "Varies by seller"],
        ["NVIDIA Jetson Orin Nano Super", "~$249", "30000-75000", "2000", "1000", "2000", "Included", "500", "35000-85000", "Various", "July 2026", "High", "SW unlock"],
        ["NVIDIA Jetson AGX Orin", "~$1999", "200000-300000", "2000", "Included", "Included", "Included", "500", "220000-320000", "Various", "July 2026", "High", ""],
        ["Raspberry Pi 5 (8GB)", "~$80", "12000-13000", "2000", "1000", "1000", "500", "500", "15000-20000", "Various", "July 2026", "High", ""],
        ["ESP32-CAM", "~$5-10", "200-800", "Included", "300", "N/A", "0", "100", "500-1500", "Various", "July 2026", "High", "Cannot run ML"]
    ]
    format_table(ws3, 3, headers3, data3)

    # ---------------- SHEET 4 ----------------
    ws4 = wb.create_sheet("Software Compatibility")
    set_title(ws4, "SOFTWARE COMPATIBILITY MATRIX", 9)
    
    devices = ["Coral Dev Board", "Coral USB", "Jetson Nano", "Jetson Orin Nano", "Jetson Orin Nano Super", "Jetson AGX Orin", "Raspberry Pi 5", "ESP32-CAM"]
    headers4 = ["Software"] + devices
    data4 = [
        ["Ubuntu", "No", "Host dep", "Ubuntu 18", "Ubuntu 22", "Ubuntu 22", "Ubuntu 22", "Ubuntu 22", "No"],
        ["Debian/Linux", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No"],
        ["Windows", "No", "Yes", "No", "No", "No", "No", "No", "No"],
        ["Python", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "MicroPython"],
        ["PyTorch", "No", "No", "Older (1.x)", "Yes", "Yes", "Yes", "Yes (CPU)", "No"],
        ["TorchVision", "No", "No", "Older", "Yes", "Yes", "Yes", "Yes (CPU)", "No"],
        ["TensorFlow", "Yes", "Yes", "Older", "Yes", "Yes", "Yes", "Yes (CPU)", "No"],
        ["TF Lite", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "TF Lite Micro"],
        ["ONNX", "No", "No", "Yes", "Yes", "Yes", "Yes", "Yes", "No"],
        ["TensorRT", "No", "No", "Yes (7.x)", "Yes (8.x+)", "Yes (8.x+)", "Yes (8.x+)", "No", "No"],
        ["OpenCV", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No"],
        ["CUDA", "No", "No", "Yes (10.2)", "Yes (12.x)", "Yes (12.x)", "Yes (12.x)", "No", "No"],
        ["cuDNN", "No", "No", "Yes", "Yes", "Yes", "Yes", "No", "No"],
        ["Edge TPU Runtime", "Yes", "Yes", "No", "No", "No", "No", "No", "No"],
        ["Docker", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No"],
        ["VS Code", "No", "Host dep", "Yes", "Yes", "Yes", "Yes", "Yes", "No"]
    ]
    format_table(ws4, 3, headers4, data4)

    # ---------------- SHEET 5 ----------------
    ws5 = wb.create_sheet("ML Model Deployment")
    set_title(ws5, "ML MODEL DEPLOYMENT ANALYSIS", 14)
    
    headers5 = ["Device", "Can use .pth directly?", "PyTorch natively?", "CUDA?", "TensorRT?", "ONNX?", "Model conversion?", "Quantization?", "TF Lite?", "Edge TPU compile?", "Deployment difficulty", "Expected Inference Speed", "Power Efficiency", "Recommended Pipeline"]
    data5 = [
        ["Coral Dev Board", "No", "No", "No", "No", "No", "Yes", "Yes (INT8)", "Yes", "Yes", "Hard", "Fast (TPU)", "Excellent", ".pth -> ONNX -> TF -> TFLite -> Quant -> TPU"],
        ["Coral USB", "No", "No", "No", "No", "No", "Yes", "Yes (INT8)", "Yes", "Yes", "Hard", "Fast (TPU)", "Excellent", "Same as above on host"],
        ["Jetson Nano", "Yes", "Yes (Older)", "Yes", "Yes", "Yes", "Optional", "Optional", "No", "No", "Medium", "Medium", "Good", ".pth -> ONNX -> TensorRT"],
        ["Jetson Orin Nano", "Yes", "Yes", "Yes", "Yes", "Yes", "Optional", "Optional", "No", "No", "Easy", "Very Fast", "Good", ".pth -> PyTorch direct OR .pth -> ONNX -> TensorRT"],
        ["Jetson Orin Nano Super", "Yes", "Yes", "Yes", "Yes", "Yes", "Optional", "Optional", "No", "No", "Easy", "Extremely Fast", "Good", ".pth -> PyTorch direct OR .pth -> ONNX -> TensorRT"],
        ["Jetson AGX Orin", "Yes", "Yes", "Yes", "Yes", "Yes", "Optional", "Optional", "No", "No", "Easy", "Overkill Fast", "Fair", ".pth -> PyTorch direct"],
        ["Raspberry Pi 5", "Yes", "Yes (CPU)", "No", "No", "Yes", "Optional", "Optional", "Optional", "No", "Easy", "Slow/Medium", "Good", ".pth -> PyTorch (CPU) OR .pth -> ONNX Runtime"],
        ["ESP32-CAM", "No", "No", "No", "No", "No", "N/A", "N/A", "N/A", "N/A", "Not Feasible", "N/A", "N/A", "NOT FEASIBLE"]
    ]
    format_table(ws5, 3, headers5, data5)

    # ---------------- SHEET 6 ----------------
    ws6 = wb.create_sheet("Edge vs IoT")
    set_title(ws6, "EDGE DEVICE VS IOT DEVICE", 3)
    
    headers6 = ["Feature", "Edge Device", "IoT Device"]
    data6 = [
        ["Definition", "Device with computing power at network edge", "Device that connects to internet to share data"],
        ["Main Purpose", "Local processing, low latency inference", "Sensing, actuating, data collection"],
        ["Data Processing Location", "Locally on the device", "Usually in the cloud"],
        ["Local AI Inference", "Yes, robust capability", "No, or very limited"],
        ["Internet Dependency", "Low (can operate offline)", "High (needs internet to function)"],
        ["Cloud Dependency", "Low", "High"],
        ["Latency", "Very Low", "Variable (depends on network)"],
        ["Bandwidth Usage", "Low (only sends results)", "High (sends raw data)"],
        ["Privacy", "High (data stays local)", "Lower (data sent to cloud)"],
        ["Power Consumption", "Medium to High", "Very Low"],
        ["Processing Power", "High (CPUs, GPUs, NPUs)", "Low (Microcontrollers)"],
        ["Storage", "GBs to TBs", "KBs to MBs"],
        ["Typical Hardware", "SBCs, Jetson, RPi", "ESP32, Arduino, Sensor Nodes"],
        ["Examples", "Jetson Orin Nano, Jetson AGX Orin, RPi 5", "ESP32, ESP32-CAM, Smart Sensors"],
        ["Camera Support", "High-res, Multi-camera CSI/USB", "Low-res, basic (e.g., OV2640)"],
        ["Sensor Support", "Yes (via GPIO)", "Yes (Excellent support)"],
        ["Network Connectivity", "Wi-Fi, Ethernet, 5G", "Wi-Fi, Bluetooth, LoRa"],
        ["AI/ML Capability", "Can run complex models (MobileNet, YOLO)", "Cannot run complex ML models"],
        ["Best Use Cases", "Real-time AI, autonomous systems", "Data collection, smart agriculture"],
        ["Advantages", "Fast, private, offline AI", "Cheap, low power, scalable"],
        ["Disadvantages", "More expensive, higher power", "Needs cloud for AI, latency"]
    ]
    format_table(ws6, 3, headers6, data6)
    
    ws6.cell(row=100, column=1).value = "Note: Edge and IoT are NOT mutually exclusive. A single system can combine both."

    # ---------------- SHEET 7 ----------------
    ws7 = wb.create_sheet("Edge + IoT Architecture")
    set_title(ws7, "EDGE + IOT ARCHITECTURE", 2)
    
    header_font = Font(name='Calibri', size=12, bold=True, color='FFFFFF')
    header_fill = PatternFill(start_color='004080', end_color='004080', fill_type='solid')

    ws7.cell(row=3, column=1).value = "Option A: Edge AI Only"
    ws7.cell(row=3, column=1).font = header_font
    ws7.cell(row=3, column=1).fill = header_fill
    
    ws7.cell(row=4, column=1).value = "Camera -> Jetson Orin Nano -> MobileNetV3 Large -> Disease Prediction -> Local Display"
    
    ws7.cell(row=6, column=1).value = "Option B: Edge AI + IoT"
    ws7.cell(row=6, column=1).font = header_font
    ws7.cell(row=6, column=1).fill = header_fill
    
    wrap_alignment = Alignment(wrap_text=True, vertical='top')
    ws7.cell(row=7, column=1).value = "Plant Leaf -> Camera -> Jetson Orin Nano -> MobileNetV3 Large -> Disease Prediction -> Local Result -> Wi-Fi -> Cloud Dashboard\nOptional sensors: Temperature, Humidity, Soil Moisture, Light via ESP32/Arduino -> Jetson or directly to cloud"
    ws7.cell(row=7, column=1).alignment = wrap_alignment
    
    headers7 = ["Component Classification", "Description"]
    data7 = [
        ["IoT components", "ESP32 sensors, Wi-Fi modules, cloud connectivity"],
        ["Edge components", "Jetson Orin Nano, camera, local processing"],
        ["AI/ML components", "MobileNetV3 Large model, inference engine"],
        ["Communication", "Wi-Fi, MQTT, HTTP"],
        ["Cloud/Software", "Dashboard, data logging, alerts"]
    ]
    format_table(ws7, 10, headers7, data7)
    ws7.column_dimensions['A'].width = 30
    ws7.column_dimensions['B'].width = 100

    # ---------------- SHEET 8 ----------------
    ws8 = wb.create_sheet("Device-by-Device Analysis")
    set_title(ws8, "DEVICE-BY-DEVICE ANALYSIS", 9)
    
    headers8 = ["Feature"] + devices
    data8 = [
        ["What is it?", "SBC with Edge TPU", "USB stick with Edge TPU", "SBC with Maxwell GPU", "SBC with Ampere GPU", "SBC with Ampere GPU (SW Unlock)", "SBC with high-end Ampere GPU", "SBC with VideoCore GPU", "MCU with Camera"],
        ["Main specs", "4 TOPS TPU", "4 TOPS TPU", "128 CUDA cores", "1024 CUDA, 40 TOPS", "1024 CUDA, 67 TOPS", "2048 CUDA, 275 TOPS", "4x A76 CPUs", "240MHz MCU"],
        ["Price range", "INR 17000-20500", "INR 7500-16000", "Variable", "INR 30000-75000", "INR 30000-75000", "INR 200k-300k", "INR 5500-13000", "INR 200-800"],
        ["OS/platforms", "Linux (Mendel)", "Linux/Mac/Win", "Ubuntu 18.04", "Ubuntu 22.04", "Ubuntu 22.04", "Ubuntu 22.04", "RPi OS, Ubuntu", "FreeRTOS"],
        ["AI frameworks", "TF Lite", "TF Lite", "Older PyTorch/TF", "PyTorch, TF, TensorRT", "PyTorch, TF, TensorRT", "PyTorch, TF, TensorRT", "PyTorch (CPU), TFLite", "TFLite Micro"],
        ["Languages", "Python, C++", "Python, C++", "Python, C++", "Python, C++", "Python, C++", "Python, C++", "Python, C++", "C++, MicroPython"],
        ["Camera support", "CSI, USB", "Via Host", "CSI, USB", "CSI, USB", "CSI, USB", "CSI, USB", "CSI, USB", "OV2640"],
        ["Connectivity", "Wi-Fi, BT, GbE", "USB", "GbE", "GbE", "GbE", "10GbE", "Wi-Fi, BT, GbE", "Wi-Fi, BT"],
        ["Strengths", "TPU speed", "Cheap TPU", "CUDA ecosystem", "Huge AI power, modern", "Best AI power/price", "Massive performance", "Cheap, community", "Ultra cheap"],
        ["Weaknesses", "EOL, hard to convert", "Requires host, EOL", "EOL, old software", "Pricey in India", "Pricey in India", "Very expensive", "No AI accelerator", "No real AI power"],
        ["Can run MobileNetV3 Large?", "Yes (with conversion)", "Yes (with conversion)", "Yes", "Yes", "Yes", "Yes", "Yes (slower)", "No"],
        ["Model conversion needed?", "Yes (Heavy)", "Yes (Heavy)", "Optional", "Optional", "Optional", "Optional", "Optional", "N/A"],
        ["Suitable for real-time plant disease detection?", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Maybe (lower FPS)", "No"],
        ["Power requirements", "5V/3A", "via USB", "5V/4A", "7-15W", "7-15W", "15-60W", "5V/5A", "5V"],
        ["Approx total project cost", "INR 20k-25k", "INR 20k-30k", "INR 18k-25k", "INR 35k-85k", "INR 35k-85k", "INR 220k-320k", "INR 15k-20k", "INR 500-1500"],
        ["Good for my project because...", "TPU is fast", "Cheap upgrade for RPi", "Has CUDA", "Perfect balance of power", "Best performance for price", "Overkill performance", "Cheap fallback option", "Good for pure IoT (no AI)"],
        ["NOT good because...", "EOL, complex conversion", "EOL, needs host", "EOL, outdated software", "Cost", "Cost", "Too expensive", "CPU only inference", "Cannot run the model"],
        ["Final recommendation", "Possible", "Recommended", "Not Recommended", "Highly Recommended", "Highly Recommended", "Recommended", "Recommended", "Not Recommended"]
    ]
    format_table(ws8, 3, headers8, data8)

    # ---------------- SHEET 9 ----------------
    ws9 = wb.create_sheet("Final Recommendation")
    set_title(ws9, "FINAL RECOMMENDATION", 14)
    
    headers9 = ["Rank", "Device", "Overall Score/10", "Performance", "Price", "PyTorch Compatibility", "Ease of Deployment", "Camera Support", "AI Capability", "Power Efficiency", "Future Expansion", "IoT Integration", "Overall Suitability", "Recommendation"]
    data9 = [
        ["1", "Jetson Orin Nano Super", "9.5", "9", "7", "10", "9", "9", "10", "8", "9", "8", "Excellent", "Highly Recommended"],
        ["2", "Jetson Orin Nano", "9.0", "8", "7", "10", "9", "9", "9", "8", "9", "8", "Excellent", "Highly Recommended"],
        ["3", "Jetson AGX Orin", "8.0", "10", "3", "10", "8", "10", "10", "5", "10", "8", "Good (Overkill)", "Recommended"],
        ["4", "RPi 5 + Coral USB", "7.5", "6", "7", "3", "6", "8", "6", "8", "7", "8", "Good", "Recommended"],
        ["5", "RPi 5 alone", "7.0", "5", "9", "6", "8", "8", "4", "8", "7", "8", "Fair", "Recommended"],
        ["6", "Coral Dev Board", "5.5", "5", "6", "2", "5", "7", "5", "9", "4", "6", "Poor (EOL)", "Possible"],
        ["7", "Jetson Nano", "4.0", "4", "5", "4", "5", "7", "4", "7", "4", "5", "Poor (EOL)", "Not Recommended"],
        ["8", "ESP32-CAM", "2.0", "1", "10", "0", "2", "3", "1", "10", "2", "7", "Not Feasible", "Not Recommended"]
    ]
    format_table(ws9, 3, headers9, data9, apply_conditional_col='N')
    
    summary_text = (
        "Final recommendation summary:\n"
        "- Best overall: Jetson Orin Nano Super Dev Kit\n"
        "- Best budget: Raspberry Pi 5 (8GB)\n"
        "- Best high-performance: Jetson AGX Orin\n"
        "- Best low-power AI: Coral USB + RPi 5\n"
        "- Not recommended: ESP32-CAM, Jetson Nano (EOL)"
    )
    ws9.cell(row=13, column=1).value = summary_text
    ws9.cell(row=13, column=1).font = Font(name='Calibri', size=12, bold=True)
    ws9.merge_cells(start_row=13, start_column=1, end_row=13, end_column=5)
    ws9.row_dimensions[13].height = 100
    ws9.cell(row=13, column=1).alignment = Alignment(wrap_text=True, vertical='top')

    # ---------------- SHEET 10 ----------------
    ws10 = wb.create_sheet("Sources and References")
    set_title(ws10, "SOURCES AND REFERENCES", 6)
    
    headers10 = ["Device", "Category", "Source Name", "URL", "Date Accessed", "Notes"]
    data10 = [
        ["NVIDIA Jetson line", "Official", "NVIDIA Developer", "developer.nvidia.com/embedded", "July 2026", ""],
        ["Google Coral line", "Official", "Coral", "coral.ai", "July 2026", "Check EOL status"],
        ["Raspberry Pi 5", "Official", "Raspberry Pi", "raspberrypi.com", "July 2026", ""],
        ["ESP32-CAM", "Official", "Espressif", "espressif.com", "July 2026", ""],
        ["All Devices", "Retail", "Robocraze", "robocraze.com", "July 2026", "Indian pricing"],
        ["All Devices", "Retail", "ThinkRobotics", "thinkrobotics.com", "July 2026", "Indian pricing"],
        ["All Devices", "Retail", "Robu.in", "robu.in", "July 2026", "Indian pricing"],
        ["All Devices", "Retail", "IndiaMART", "indiamart.com", "July 2026", "Wholesale pricing"]
    ]
    format_table(ws10, 3, headers10, data10)

    # Save
    wb.save('/home/beldar-vishesh/Desktop/IOT project /Plant_Disease_Edge_AI_IoT_Device_Comparison.xlsx')

if __name__ == '__main__':
    main()
