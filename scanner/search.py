"""
search images by similarity.
runs a server to minimize image rehashing.
"""

import imagehash
from PIL import Image
from data import cards
from . import util

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