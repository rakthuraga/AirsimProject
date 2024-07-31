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

def extract_coordinates(text):
    pattern = re.compile(r'\(\d+%?, \d+%?\)')
    coordinates = pattern.findall(text)
    return coordinates

# Function to extract qualitative descriptions using NLTK
def extract_qualitative_descriptions(text):
    # Tokenize the text
    tokens = nltk.word_tokenize(text)
    
    # Perform part-of-speech tagging
    tagged_tokens = nltk.pos_tag(tokens)

    # Define a chunk grammar to find adjective-noun phrases
    grammar = r"ADJ_NOUN: {<JJ><NN|NNS>}"

    # Create a chunk parser
    chunk_parser = nltk.RegexpParser(grammar)
    
    # Parse the tagged tokens to find chunks
    chunks = chunk_parser.parse(tagged_tokens)

     # Extract qualitative descriptions
    descriptions = []
    for subtree in chunks.subtrees(filter=lambda t: t.label() == 'ADJ_NOUN'):
        description = " ".join(word for word, pos in subtree.leaves())
        descriptions.append(description)
    
    return descriptions

prompt_coordinates = ("In the following image, the cameras are positioned as follows:\n\
                    Top left: Left Front (LF) camera\n\
                    Top right: Right Front (RF) camera\n\
                    Middle left: Left Down (LD) camera\n\
                    Middle right: Right Down (RD) camera\n\
                    Bottom left: Left Back (LB) camera\n\
                    Bottom right: Right Back (RB) camera \
                    Please analyze the following image and identify the location of the specified object using percentage-based coordinates. The coordinates should represent the position of the object relative to the dimensions of the image:\
                    - 0% horizontally means the object is at the far left of the image.\
                    - 100% horizontally means the object is at the far right of the image.\
                    - 0% vertically means the object is at the top of the image.\
                    - 100% vertically means the object is at the bottom of the image.\
                    Provide the coordinates in the format (horizontal_percentage, vertical_percentage). For example, if an object is located at the center of the image, the coordinates should be (50%, 50%). If an object is located at the bottom-right corner, the coordinates should be (100%, 100%).\
                    The object I want you to do this for is the house in the left back camera")