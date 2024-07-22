import base64
import requests
from datetime import datetime
import json
import os

# OpenAI API Key
api_key = "your-api-key-make-sure-has-gpt4-enabled"  # Ensure you use your actual API key

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')