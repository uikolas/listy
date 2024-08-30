import os
import requests


def upload(file):
    params = {'key': os.environ.get('IMGBB_API_KEY')}
    files = {'image': file}
    request = requests.post('https://api.imgbb.com/1/upload', files=files, params=params)
    json = request.json()

    return json['data']['url']