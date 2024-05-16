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

    try:
        # Open the image using PIL
        image = Image.open(image_file)

        # Convert the image to bytes for Google Vision API
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        content = img_byte_arr.getvalue()

        # Perform object detection using Google Vision API
        image = vision.Image(content=content)
        response = vision_client.object_localization(image=image)
        objects = response.localized_object_annotations

        # Collect object names and bounding boxes
        object_details = [{'name': obj.name, 'score': obj.score} for obj in objects]

        # Create a prompt with the object details and the question
        object_names = ', '.join([obj['name'] for obj in object_details])
        prompt = (
            f"The following objects were detected in the image: {object_names}\n\n"
            f"Question: {question}"
        )

        # Call the OpenAI API
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ])

        analysis = response.choices[0].message.content.strip()

        return jsonify({
            'objects': object_details,
            'analysis': analysis
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

   
   