import gradio as gr
import main  # Assuming your main.py is named `main` and in the same folder
import json
from loguru import logger

def video_identity(video_file):
    video_path = video_file.name  # Get the path of the uploaded video
    logger.add("app.log", rotation="1 MB", level="INFO")

    try:
        # Call the `main.main` function with the uploaded video file
        main.main(video_path)  # This will trigger your existing processing logic

        # Assuming `main.main` creates an output JSON file with the results
        with open("output.json", "r") as f:
            output = json.load(f)

        # Return the results and log file for download
        return json.dumps(output), "app.log"
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"error": str(e)}, "app.log"

# Gradio interface
demo = gr.Interface(
    fn=video_identity,
    inputs=gr.File(label="Upload Video File"),
    outputs=[
        gr.JSON(label="Detection Results"),  # Outputs the detection results in JSON
        gr.File(label="Download Log File")  # Provides the log file for download
    ],
    title="Logo Detection in Videos",
    description="Upload a video to detect Pepsi and Coca-Cola logos."
)

if __name__ == "__main__":
    demo.launch()
