import torch
import torch.nn as nn
import torchvision.models as models
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_plant_model(model_name="mobilenet_v3_large", num_classes=15, pretrained=True, freeze_backbone=True):
    """
    Returns a MobileNet model modified for the specified number of target classes.
    """
    if model_name == "mobilenet_v3_large":
        # Load MobileNetV3 Large
        if pretrained:
            weights = models.MobileNet_V3_Large_Weights.DEFAULT
            model = models.mobilenet_v3_large(weights=weights)
            logging.info("Loaded pretrained MobileNetV3 Large.")
        else:
            model = models.mobilenet_v3_large()
            logging.info("Loaded un-trained MobileNetV3 Large.")
            
        # Get the input features of the last layer in classifier
        in_features = model.classifier[3].in_features
        
        # Replace the final linear layer (index 3 in MobileNetV3 Large classifier)
        model.classifier[3] = nn.Linear(in_features, num_classes)
        
    elif model_name == "mobilenet_v2":
        # Load MobileNetV2
        if pretrained:
            weights = models.MobileNet_V2_Weights.DEFAULT
            model = models.mobilenet_v2(weights=weights)
            logging.info("Loaded pretrained MobileNetV2.")
        else:
            model = models.mobilenet_v2()
            logging.info("Loaded un-trained MobileNetV2.")
            
        # Replace the final linear layer in the classifier
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, num_classes)
        
    else:
        raise ValueError(f"Unsupported model name: {model_name}. Choose 'mobilenet_v3_large' or 'mobilenet_v2'.")

    # Freeze pretrained feature backbone layers initially if requested
    if pretrained and freeze_backbone:
        freeze_model_backbone(model, model_name)
        
    # Print classifier output dimension and trainable params
    if model_name == "mobilenet_v3_large":
        out_features = model.classifier[3].out_features
    else:
        out_features = model.classifier[1].out_features
        
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    logging.info(f"[DEBUG] Model initialized: {model_name}")
    logging.info(f"[DEBUG] Classifier Output Dimension: {out_features}")
    logging.info(f"[DEBUG] Total Parameters: {total_params:,} | Trainable Parameters: {trainable_params:,}")
        
    return model

def freeze_model_backbone(model, model_name):
    """
    Freezes all parameters of the model backbone, keeping only the final classifier head trainable.
    """
    logging.info("Freezing model backbone layers...")
    for param in model.parameters():
        param.requires_grad = False
        
    # Unfreeze the classifier head specifically
    if model_name == "mobilenet_v3_large":
        for param in model.classifier.parameters():
            param.requires_grad = True
    elif model_name == "mobilenet_v2":
        for param in model.classifier.parameters():
            param.requires_grad = True
            
    logging.info("Backbone frozen. Classifier head is active and trainable.")

def unfreeze_model_backbone(model):
    """
    Unfreezes all parameters in the model for fine-tuning.
    """
    logging.info("Unfreezing all model layers for fine-tuning...")
    for param in model.parameters():
        param.requires_grad = True
    logging.info("All layers unfrozen.")
