# src/model.py
from ultralytics import YOLO
from loguru import logger
import os

def load_model(model_path):
    try:
        # Update path to point to the model directory
        model = YOLO(os.path.join("model", model_path), verbose=False)  
        logger.info("Model loaded successfully.")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise
