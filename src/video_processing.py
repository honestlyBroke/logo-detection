# video_processing.py
import os
import json
from loguru import logger
import av
from frame_processing import process_frame
from utils import NumpyEncoder


def append_to_json(pepsi_pts, cocacola_pts, output_path="output.json"):
    try:
        if os.path.exists(output_path):
            with open(output_path, "r") as f:
                output = json.load(f)
        else:
            output = {
                "Pepsi_pts": [],
                "Pepsi_details": [],
                "CocaCola_pts": [],
                "CocaCola_details": [],
            }

        # Update output in the desired order
        output["Pepsi_pts"].extend([entry["timestamp"] for entry in pepsi_pts])
        output["Pepsi_details"].extend(pepsi_pts)

        output["CocaCola_pts"].extend([entry["timestamp"] for entry in cocacola_pts])
        output["CocaCola_details"].extend(cocacola_pts)

        with open(output_path, "w") as f:
            json.dump(output, f, indent=4, cls=NumpyEncoder)
        logger.info("Output JSON updated successfully.")
    except Exception as e:
        logger.error(f"Error updating JSON: {e}")
        raise


def process_video(video_path, model, threshold, class_name_mapping, output_json_path):
    try:
        container = av.open(video_path)
        pepsi_pts = []
        cocacola_pts = []
        last_processed_second = -1

        for frame in container.decode(video=0):
            timestamp = float(frame.pts * frame.time_base)
            current_second = int(round(timestamp))
            if current_second == last_processed_second:
                continue  # Skip frames within the same second
            last_processed_second = current_second
            frame_pepsi_pts, frame_cocacola_pts = process_frame(frame, timestamp, model, threshold, class_name_mapping)
            pepsi_pts.extend(frame_pepsi_pts)
            cocacola_pts.extend(frame_cocacola_pts)

            # Append results to JSON file after processing each frame
            append_to_json(frame_pepsi_pts, frame_cocacola_pts, output_json_path)
        return pepsi_pts, cocacola_pts
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        raise
