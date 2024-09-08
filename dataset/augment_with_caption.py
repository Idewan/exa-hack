import base64
import os
import requests

api_key = os.getenv("API_KEY_HACKATHON")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.64encode(image_file.read()).decode('utf-8')

for dirs in os.listdir("data/"):
    
