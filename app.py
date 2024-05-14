from flask import Flask, request, jsonify
from PIL import Image
import io
from openai import OpenAI

client = OpenAI(api_key='your_openai_api_key_here')
from google.cloud import vision
import os

app = Flask(__name__)