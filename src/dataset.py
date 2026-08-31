import os
import json
import logging
from pathlib import Path
from PIL import Image
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PlantDataset(Dataset):
    """
    Custom PyTorch Dataset for Plant Disease Detection.
    """
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        label = self.labels[idx]
        
        try:
            # Load image and ensure it's in RGB mode
            with open(img_path, 'rb') as f:
                img = Image.open(f)
                img = img.convert('RGB')
        except Exception as e:
            logging.error(f"Error loading image {img_path}: {e}")
            # Return a dummy tensor or re-raise
            raise RuntimeError(f"Corrupted or invalid image: {img_path}") from e

        if self.transform:
            img = self.transform(img)

        return img, label

def get_transforms(img_size=224):
    """
    Returns train and val/test torchvision transforms.
    MobileNet models expect 224x224 input sizes by default.
    """
    train_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomResizedCrop(img_size, scale=(0.8, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(15),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.95, 1.05)),
        transforms.RandomPerspective(distortion_scale=0.1, p=0.3),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_test_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.CenterCrop(img_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_test_transform

def verify_and_split_dataset(dataset_dir, val_split=0.15, test_split=0.15, random_seed=42):
    """
    Scans the dataset directory, detects all classes, splits images into train, val, and test,
    and returns lists of file paths and labels for each split, along with class mapping.
    """
    dataset_path = Path(dataset_dir)
    if not dataset_path.exists() or not dataset_path.is_dir():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")
        
    # Detect classes (subdirectories)
    classes = sorted([d.name for d in dataset_path.iterdir() if d.is_dir()])
    if not classes:
        raise ValueError(f"No class folders found in dataset directory: {dataset_dir}")
        
    class_to_idx = {class_name: idx for idx, class_name in enumerate(classes)}
    logging.info(f"Detected {len(classes)} classes: {classes}")
    
    image_paths = []
    labels = []
    
    # Supported image extensions
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.JPG', '.JPEG', '.PNG', '.BMP'}
    
    for class_name in classes:
        class_dir = dataset_path / class_name
        class_idx = class_to_idx[class_name]
        
        # List all files in the class folder
        class_files = [f for f in class_dir.iterdir() if f.is_file() and f.suffix in valid_extensions]
        
        if not class_files:
            logging.warning(f"No valid images found in directory: {class_dir}")
            continue
            
        for file_path in class_files:
            image_paths.append(str(file_path))
            labels.append(class_idx)
            
    if not image_paths:
        raise ValueError("No images found in any of the class directories.")
        
    logging.info(f"Total images found before deduplication: {len(image_paths)}")
    
    # Deduplicate by file content hash to prevent data leakage across splits.
    # The PlantVillage dataset contains content-identical images with different filenames.
    import hashlib
    seen_hashes = set()
    unique_paths = []
    unique_labels = []
    duplicates_removed = 0
    
    for path, label in zip(image_paths, labels):
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            for block in iter(lambda: f.read(65536), b''):
                h.update(block)
        file_hash = h.hexdigest()
        
        if file_hash not in seen_hashes:
            seen_hashes.add(file_hash)
            unique_paths.append(path)
            unique_labels.append(label)
        else:
            duplicates_removed += 1
            
    image_paths = unique_paths
    labels = unique_labels
    
    if duplicates_removed > 0:
        logging.info(f"[DEDUP] Removed {duplicates_removed} content-identical duplicate images.")
    logging.info(f"Total verified unique images: {len(image_paths)}")
    
    # Stratified split to maintain class distributions
    # First split off train set
    temp_split = val_split + test_split
    train_paths, temp_paths, train_labels, temp_labels = train_test_split(
        image_paths, labels, test_size=temp_split, random_state=random_seed, stratify=labels
    )
    
    # Then split temp into val and test
    val_ratio_of_temp = val_split / temp_split
    val_paths, test_paths, val_labels, test_labels = train_test_split(
        temp_paths, temp_labels, test_size=(1 - val_ratio_of_temp), random_state=random_seed, stratify=temp_labels
    )
    
    # Verify that all splits contain all target classes
    train_unique_classes = set(train_labels)
    val_unique_classes = set(val_labels)
    test_unique_classes = set(test_labels)
    
    logging.info(f"[DEBUG] Verification: train has {len(train_unique_classes)} classes, val has {len(val_unique_classes)} classes, test has {len(test_unique_classes)} classes.")
    if len(train_unique_classes) != len(classes) or len(val_unique_classes) != len(classes) or len(test_unique_classes) != len(classes):
        logging.warning("[WARNING] Some classes are missing from train, validation, or test sets!")
    else:
        logging.info("[DEBUG] Split stratification verified successfully. All splits contain all classes.")

    # Count and print per-class distribution across train, validation, and test splits
    from collections import Counter
    train_counts = Counter(train_labels)
    val_counts = Counter(val_labels)
    test_counts = Counter(test_labels)
    
    print("\n" + "="*70)
    print(f"{'Class Name':<45} | {'Train':<6} | {'Val':<5} | {'Test':<5}")
    print("="*70)
    for class_name, idx in class_to_idx.items():
        print(f"{class_name:<45} | {train_counts[idx]:<6} | {val_counts[idx]:<5} | {test_counts[idx]:<5}")
    print("="*70 + "\n")

    logging.info(f"Dataset Split Summary:")
    logging.info(f"Train set: {len(train_paths)} images")
    logging.info(f"Validation set: {len(val_paths)} images")
    logging.info(f"Test set: {len(test_paths)} images")
    
    return (train_paths, train_labels), (val_paths, val_labels), (test_paths, test_labels), class_to_idx

def get_dataloaders(dataset_dir, batch_size=32, img_size=224, num_workers=4):
    """
    Creates PyTorch DataLoaders for train, validation, and test splits.
    """
    splits = verify_and_split_dataset(dataset_dir)
    (train_paths, train_labels), (val_paths, val_labels), (test_paths, test_labels), class_to_idx = splits
    
    train_transform, val_test_transform = get_transforms(img_size)
    
    train_dataset = PlantDataset(train_paths, train_labels, transform=train_transform)
    val_dataset = PlantDataset(val_paths, val_labels, transform=val_test_transform)
    test_dataset = PlantDataset(test_paths, test_labels, transform=val_test_transform)
    
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True,
        num_workers=num_workers, pin_memory=torch.cuda.is_available()
    )
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=torch.cuda.is_available()
    )
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=torch.cuda.is_available()
    )
    
    return train_loader, val_loader, test_loader, class_to_idx
