import cv2
import tensorflow as tf
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('fill in with your openai api key')

client = OpenAI(api_key=api_key)

# Initialize OpenAI API key

# Load the pre-trained model from the local directory
model_dir = '/Users/sumalathaodati/Desktop/rhomanApi/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/saved_model'
model = tf.saved_model.load(model_dir)

# Function to load image
def load_image_into_numpy_array(path):
    return np.array(cv2.imread(path))

# Function to detect objects
def detect_objects(image_path):
    image_np = load_image_into_numpy_array(image_path)
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]

    detections = model(input_tensor)
    return detections