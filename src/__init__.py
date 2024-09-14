# src/__init__.py

"""
src package

This package includes modules for:
- Video processing (`video_processing.py`)
- Frame processing (`frame_processing.py`)
- Model handling (`model.py`)
- Gradio application (`app.py`)

Modules:
- process_video: Handles video processing tasks
- process_frame: Processes individual video frames
- load_model: Loads the YOLOv8 model
- app: Gradio application for user interface
"""

# Optional: Import specific functions or classes
from .video_processing import process_video
from .frame_processing import process_frame
from .model import load_model