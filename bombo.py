import base64
import requests
import json
import os
from datetime import datetime

# OpenAI API Key
api_key = "put-your-api-key"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')