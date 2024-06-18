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
    
# Function to save the question and response to a file
def save_result(question, response, filename="result.json"):
    data = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "response": response
    }
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Path to your image
image_path = "test_image.png"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

question = "is the jackson and smith building closer to me or the wheelchair signs on the floor?"

payload = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": question
        },
        {
            "role": "system",
            "content": f"Image data: {base64_image}"
        }
    ],
    "max_tokens": 300
}