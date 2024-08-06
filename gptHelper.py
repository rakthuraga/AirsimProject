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

# Save the updated data back to the file
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Function to analyze the image using GPT-4
def analyze_image(image_path, question):
    base64_image = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": question},
            {"role": "user", "content": {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}}
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()
    response_message = response_data['choices'][0]['message']['content'].strip()
    return response_message