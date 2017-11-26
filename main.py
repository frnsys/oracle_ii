import requests
import numpy as np
from detect import detect
from db import DB

db = DB('collection.db')

def on_detect(card_image):
    image = np.array(card_image).tolist()
    resp = requests.post('http://localhost:8888',
                         json={'image': image, 'max_distance': 10000})
    results = resp.json()['results']
    if results:
        result = results[0]
        print('{} ({})'.format(result['card']['name'], result['id']))
        db.append(result['id'])


if __name__ == '__main__':
    detect(on_detect)

