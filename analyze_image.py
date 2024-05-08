import cv2
import tensorflow as tf
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('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')

client = OpenAI(api_key=api_key)

