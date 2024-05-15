from flask import Flask, request, jsonify
from PIL import Image
import io
from openai import OpenAI

client = OpenAI(api_key='your_openai_api_key_here')
from google.cloud import vision
import os

app = Flask(__name__)

# Initialize OpenAI API key

# Set up Google Cloud Vision client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_service_account_key.json'
vision_client = vision.ImageAnnotatorClient()

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    # Check if an image file is present in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    # Check if a question is provided
    if 'question' not in request.form:
        return jsonify({'error': 'No question provided'}), 400
    
    image_file = request.files['image']
    question = request.form['question']