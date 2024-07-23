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
    
# Function to save the question and response to a file
def save_result(question, response, image_path, filename="result.json"):
    # Load existing data from the file
    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = json.load(file)
            if not isinstance(data, list):
                data = []
    else:
        data = []

# Extract the image name from the image path
    image_name = os.path.basename(image_path)

    # Append the new result
    data.append({
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "response": response,
        "referenced_image": image_name
    })