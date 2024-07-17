import base64
import requests
from datetime import datetime
import json
import os
import nltk
import re

# OpenAI API Key
api_key = "fill-in-with-your-api-key"

# This function checks if the necessary NLTK data packages are installed.
# If a package is missing, it will automatically download it.
def check_and_download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')

    try:
        nltk.data.find('chunkers/maxent_ne_chunker')
    except LookupError:
        nltk.download('maxent_ne_chunker')

    try:
        nltk.data.find('corpora/words')
    except LookupError:
        nltk.download('words')

    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

# Ensure NLTK data is available
check_and_download_nltk_data()