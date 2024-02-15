import requests
import os
import config
import json
from exceptions import ForeignApiError


def get_weather(latitude: float, longtitude: float) -> dict:
    headers = {'X-Yandex-API-Key': os.environ.get('YANDEX_KEY')}
    coordinates = {'lat': latitude, 'lon': longtitude}
    response = requests.get(config.YANDEX_URL, headers=headers, params=coordinates)
    if response.status_code != config.OK:
        raise ForeignApiError('Yandex.Weather', response.status_code)
    return json.loads(response.content)
