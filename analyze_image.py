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