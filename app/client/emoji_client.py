import os
import requests
from app.exceptions import ClientException


def search_emoji(keyword):
    params = {'search': keyword, 'access_key': os.environ.get('EMOJI_API_KEY')}
    request = requests.get('https://emoji-api.com/emojis', params)
    json = request.json()

    if 'status' in json and json['status'] == 'error':
        raise ClientException('Failed to find')

    return json[0]['character']
