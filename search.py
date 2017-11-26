"""
search images by similarity.
runs a server to minimize image rehashing.
"""

import util
import imagehash
import numpy as np
from PIL import Image
from data import cards

HASH_SIZE = 128 # must be a power of 2


def create_index(fnames, ids):
    """create similarity index"""
    idx = {}
    hashes = util.run_parallel(fnames, imghash)
    for id, hash in zip(ids, hashes):
        idx[id] = hash
    return idx


def imghash(fname):
    """generate perceptual hash for image.
    uses whash, but other options are available:
    <https://github.com/JohannesBuchner/imagehash>"""
    img = Image.open(fname)
    return imagehash.whash(img, hash_size=HASH_SIZE)


def search(img, idx, max_distance=50, top_n=3):
    """was using faiss, but kept getting segmentation fault.
    brute force search instead"""
    hash = imagehash.whash(img, hash_size=HASH_SIZE)
    results = []
    for id, h in idx.items():
        dist = hash - h
        if dist < max_distance:
            results.append({'id': id, 'dist': dist, 'card': cards[id]})
    return sorted(results, key=lambda r: r['dist'])[:top_n]


if __name__ == '__main__':
    from data import fnames, mids
    from flask import Flask, request, jsonify

    print('preparing index...')
    idx = create_index(fnames, mids)

    print('starting server...')
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def query():
        data = request.get_json()
        dist = data['max_distance']
        img = np.array(data['image']).astype('uint8')
        img = Image.fromarray(img)
        results= search(img, idx, max_distance=dist)
        return jsonify(results=results)

    app.run(port=8888)