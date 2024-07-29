# Training Data for Logo Detection

This document outlines the steps taken to train the logo detection model using Google Colab. The `logo_detection.ipynb` file included in this repository serves as a reference.

## Steps for Training the Model

### 1. Setting Up the Environment

Firstly, we need to change the runtime machine to ensure that GPU is used for training. We used Tesla T4 for our model.

#### Checking GPU Information

```bash
!nvidia-smi
```

### 2. Installing Required Libraries

Install `ultralytics` and check the version details. We used YOLOv8.2.67, the latest version.

```bash
%pip install ultralytics
import ultralytics
ultralytics.checks()
```

### 3. Importing the Dataset from Roboflow

Install the `roboflow` library and import the dataset.

```bash
!pip install roboflow
from roboflow import Roboflow
rf = Roboflow(api_key="YOUR API KEY")
project = rf.workspace("videoverse-s3lki").project("pc-e4adv")
version = project.version(1)
dataset = version.download("yolov8")
```

Rename and set up the correct paths in `data.yaml` for the dataset.

### 4. Training the Model

Train the model using the following command. We chose the medium model (`yolov8m.pt`) and set it to train for 20 epochs with an image size of 640.

```bash
!yolo task=detect mode=train model=yolov8m.pt data={dataset.location}/data.yaml epochs=20 imgsz=640
```

You can change the model according to the resources you have.

### 5. Plotting the Confusion Matrix

Plot the confusion matrix to check the data.

```python
from IPython.display import Image
Image(filename=f"/content/runs/detect/train/confusion_matrix.png", width=600)
```

### 6. Checking the Results

Check the training results.

```python
from IPython.display import Image
Image(filename=f"/content/runs/detect/train/results.png", width=600)
```

### 7. Running the Detection Test

Run the detect test using the trained model.

```bash
!yolo task=detect mode=val model=/content/runs/detect/train/weights/best.pt data={dataset.location}/data.yaml
```

### 8. Running Against Test Data

Run the model against the test data.

```bash
!yolo task=detect mode=predict model=/content/runs/detect/train/weights/best.pt conf=0.5 source={dataset.location}/test/images
```

### 9. Checking the Predicted Data

Check the predicted data.

```python
import glob
from IPython.display import Image, display

for image_path in glob.glob('/content/runs/detect/predict/*.jpg'):
    display(Image(filename=image_path, width=600))
    print("\n")
```

### 10. Downloading the Trained Model

The trained model is saved in the path `/runs/weights` as `best.pt`. Download it and rename it to `logo-detect.pt` for ease of use.
