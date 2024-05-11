import cv2
import tensorflow as tf
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('fill in with your openai api key')

client = OpenAI(api_key=api_key)

# Initialize OpenAI API key

# Load the pre-trained model from the local directory
model_dir = '/Users/sumalathaodati/Desktop/rhomanApi/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/saved_model'
model = tf.saved_model.load(model_dir)

# Function to load image
def load_image_into_numpy_array(path):
    return np.array(cv2.imread(path))

# Function to detect objects
def detect_objects(image_path):
    image_np = load_image_into_numpy_array(image_path)
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]

    detections = model(input_tensor)
    return detections

# Function to draw bounding boxes
def draw_bounding_boxes(image_np, detections):
    h, w, _ = image_np.shape
    boxes = detections['detection_boxes'][0].numpy()
    scores = detections['detection_scores'][0].numpy()
    classes = detections['detection_classes'][0].numpy().astype(np.int64)

    for i in range(boxes.shape[0]):
        if scores[i] > 0.5:
            box = boxes[i] * [h, w, h, w]
            box = box.astype(np.int32)
            image_np = cv2.rectangle(image_np, (box[1], box[0]), (box[3], box[2]), (0, 255, 0), 2)

    return image_np, scores, classes

# Function to analyze objects
def analyze_objects(scores, classes):
    labels = {
        1: 'pedestrian', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'aircraft',
        6: 'bus', 7: 'subway train', 8: 'delivery truck', 9: 'boat', 10: 'traffic signal',
        11: 'fire hydrant', 13: 'stop sign', 14: 'parking meter', 15: 'public bench',
        16: 'bird', 17: 'stray cat', 18: 'stray dog', 19: 'mounted police', 20: 'street vendor',
        21: 'urban cow', 22: 'advertisement billboard', 23: 'police barricade', 24: 'road construction sign', 25: 'pedestrian bridge',
        27: 'backpack', 28: 'umbrella', 31: 'briefcase', 32: 'tie', 33: 'rolling suitcase',
        34: 'street performer', 35: 'skateboarder', 36: 'snowboarder', 37: 'street vendor cart', 38: 'kite',
        39: 'street sign', 40: 'security camera', 41: 'electric scooter', 42: 'drone',
        43: 'construction worker', 44: 'bottle', 46: 'coffee cup', 47: 'takeout cup', 48: 'fork',
        49: 'knife', 50: 'spoon', 51: 'food container', 52: 'banana', 53: 'apple',
        54: 'sandwich', 55: 'orange', 56: 'broccoli', 57: 'carrot', 58: 'hot dog vendor',
        59: 'pizza slice', 60: 'donut', 61: 'cake', 62: 'public chair', 63: 'couch',
        64: 'potted plant', 65: 'bed', 67: 'dining table', 70: 'public restroom', 72: 'billboard',
        73: 'laptop', 74: 'mouse', 75: 'remote', 76: 'keyboard', 77: 'smartphone',
        78: 'microwave', 79: 'oven', 80: 'toaster', 81: 'sink', 82: 'vending machine',
        84: 'newspaper', 85: 'clock', 86: 'flower pot', 87: 'scissors'
    }
    detected_objects = [labels[cls] for i, cls in enumerate(classes) if scores[i] > 0.5]
    if not detected_objects:
        description = "No objects with high confidence were detected in the image."
    else:
        description = f"The image contains the following objects: {', '.join(detected_objects)}."

    response = client.chat.completions.create(model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Analyze the following objects detected in an image: {description}"}
    ],
    max_tokens=150)

    return response.choices[0].message.content.strip()

# Process the image
image_path = 'testImage.jpeg'
detections = detect_objects(image_path)
image_np = load_image_into_numpy_array(image_path)
image_with_boxes, scores, classes = draw_bounding_boxes(image_np, detections)
cv2.imwrite('output_image.png', image_with_boxes)