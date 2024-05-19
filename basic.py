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