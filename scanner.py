import requests
import numpy as np
from db import DB
from scanner import search
from scanner.detect import detect

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
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'search':

        from data import fnames, mids
        from flask import Flask, request, jsonify

        print('preparing index...')
        idx = search.create_index(fnames, mids)

        print('starting server...')
        app = Flask(__name__)

        @app.route('/', methods=['POST'])
        def query():
            data = request.get_json()
            dist = data['max_distance']
            img = np.array(data['image']).astype('uint8')
            img = search.Image.fromarray(img)
            results= search.search(img, idx, max_distance=dist)
            return jsonify(results=results)

        app.run(port=8888)

    else:
        detect(on_detect)

