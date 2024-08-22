import os
import requests
from dotenv import load_dotenv

load_dotenv()

import requests

def detect_faces(file_path):
     with open(file_path, 'rb') as file:
        facecloud_api_url = os.getenv('FACECLOUD_API_URL')
        facecloud_api_jwt = os.getenv('FACECLOUD_API_JWT')
        params = {
            'demographics': 'true'
            }
        headers = {
            'Content-Type': 'image/jpeg',
            'Authorization': f'Bearer {facecloud_api_jwt} '
            }
        response = requests.request("POST", facecloud_api_url, headers=headers, data=file, params=params)
        response.raise_for_status()
        faces = response.json().get('data', [])
        return [{
        'bounding_box': face['bbox'],
        'gender': face['demographics']['gender'],
        'age': face['demographics']['age']['mean']
        } for face in faces]