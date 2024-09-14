# src/main.py
import sys
from video_processing import process_video
from model import load_model
from utils import format_timestamp
from loguru import logger

def main(video_path):
    model_path = "logo-detect.pt"  # Path relative to the `model` directory
    output_json_path = "output.json"
    threshold = 0.5

    # Define a mapping between the model's class names and the code's class names
    class_name_mapping = {
        "PEPSI": "pepsi",
        "COCA-COLA": "coke",
    }

    # Configure logger
    logger.add("app.log", rotation="1 MB", level="INFO")

    # Load model
    model = load_model(model_path)

    try:
        pepsi_pts, cocacola_pts = process_video(video_path, model, threshold, class_name_mapping, output_json_path)
        logger.info(f"Pepsi points: {pepsi_pts}")
        logger.info(f"CocaCola points: {cocacola_pts}")
        logger.info("JSON updated successfully.")
    except Exception as e:
        logger.error(f"An error occurred in the main workflow: {e}")
        raise

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python main.py <video_path>")
        sys.exit(1)
    video_path = sys.argv[1]
    main(video_path)
