import os
import glob
import zipfile
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def reassemble_and_extract_dataset(output_zip="PlantVillage.zip", extract_dir="PlantVillage"):
    """
    Reassembles multipart dataset chunks and unzips the dataset directory.
    """
    parts = sorted(glob.glob("PlantVillage.zip.part_*"))
    if not parts and not os.path.exists(output_zip):
        logging.error("No dataset parts (PlantVillage.zip.part_*) or PlantVillage.zip found.")
        return False
        
    if parts and (not os.path.exists(output_zip) or os.path.getsize(output_zip) < 300 * 1024 * 1024):
        logging.info(f"Found {len(parts)} split dataset parts. Reassembling {output_zip}...")
        with open(output_zip, "wb") as outfile:
            for part in parts:
                logging.info(f"Merging {part}...")
                with open(part, "rb") as infile:
                    outfile.write(infile.read())
        logging.info(f"Reassembly complete: {output_zip} ({os.path.getsize(output_zip) / (1024*1024):.1f} MB)")
        
    if not os.path.exists(extract_dir):
        logging.info(f"Extracting {output_zip} -> ./{extract_dir}...")
        with zipfile.ZipFile(output_zip, 'r') as zip_ref:
            zip_ref.extractall(".")
        logging.info("Extraction complete. Dataset ready!")
    else:
        logging.info(f"Dataset directory '{extract_dir}' already exists.")
    return True

if __name__ == "__main__":
    reassemble_and_extract_dataset()
