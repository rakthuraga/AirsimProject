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