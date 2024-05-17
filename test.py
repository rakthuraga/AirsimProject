import requests

url = 'http://127.0.0.1:5000/analyze-image'
image_path = 'test_image.png'  # Replace with the path to your test image
question = 'What is in this image?'

with open(image_path, 'rb') as image_file:
    files = {'image': image_file}
    data = {'question': question}
    response = requests.post(url, files=files, data=data)

print(response.json())
