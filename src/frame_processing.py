# frame_processing.py
from model import load_model
from utils import format_timestamp
from loguru import logger
import numpy as np


def process_frame(frame, timestamp, model, threshold, class_name_mapping):
    try:
        img = frame.to_image()
        formatted_timestamp = format_timestamp(timestamp)
        logger.info(f"Processing frame at timestamp: {formatted_timestamp}")

        results = model(img)  # Run inference
        logger.info(f"Inference results: {results}")

        pepsi_pts = []
        cocacola_pts = []

        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs
            logger.info(f"Boxes detected: {boxes}")

            for box in boxes:
                # Extract the bounding box and confidence
                x1, y1, x2, y2 = [round(coord, 2) for coord in box.xyxy[0].tolist()]  # Convert to list with limited precision
                score = round(box.conf[0].item(), 2)  # Convert to float with limited precision
                class_id = int(box.cls[0].item())  # Convert to int
                logger.info(f"Detected box with score {score} and class ID {class_id}")
                logger.info(result.names)
                if score > threshold:
                    class_name = result.names[class_id].split(" ", maxsplit=1)[0].upper()
                    width = round(x2 - x1, 2)
                    height = round(y2 - y1, 2)
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    frame_center_x = img.width / 2
                    frame_center_y = img.height / 2
                    distance_from_center = round(
                        ((center_x - frame_center_x) ** 2
                         + (center_y - frame_center_y) ** 2) ** 0.5, 2)

                    entry = {
                        "timestamp": formatted_timestamp,
                        "size": {"width": width, "height": height},
                        "distance_from_center": distance_from_center,
                    }
                    logger.info(f"Entry created: {entry}")

                    if class_name == class_name_mapping["PEPSI"].upper():
                        pepsi_pts.append(entry)
                    elif class_name == class_name_mapping["COCA-COLA"].upper():
                        cocacola_pts.append(entry)

        return pepsi_pts, cocacola_pts
    except Exception as e:
        logger.error(f"Error processing frame: {e}")
        raise
