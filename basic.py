import os
import base64
import requests
from dotenv import load_dotenv
import cv2
import tensorflow as tf
import numpy as np
from openai import OpenAI


# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv('api-key')
client = OpenAI(api_key=api_key)

if api_key is None:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

print(f"Loaded API key: {api_key}")  # Debugging line to verify API key loading

def encode_image(image_path):
    """Encodes the image to base64 format."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')