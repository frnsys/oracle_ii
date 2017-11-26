import imagehash
import numpy as np
from PIL import Image
from faiss import faiss

HASH_SIZE = 16 # must be power of 2
D = HASH_SIZE**2


def create_index(fnames, ids):
    """create similarity index"""
    # <https://github.com/facebookresearch/faiss/wiki/Faiss-indexes>
    # idx_ = faiss.IndexLSH(d, 2048) # this gets better more bits
    # idx_ = faiss.IndexFlatL2(d) # best, but brute-force, and stores full vectors
    idx_ = faiss.IndexFlatIP(D) # might be best option?
    # see <https://github.com/facebookresearch/faiss/wiki/Getting-started-tutorial>

    idx = faiss.IndexIDMap(idx_) # so we can specify our own indices
    hashes = [imghash(fname) for fname in fnames]
    hashes = np.stack(hashes)

    idx.add_with_ids(hashes, np.array(ids))
    return idx


def imghash(fname):
    """generate perceptual hash for image.
    uses whash, but other options are available:
    <https://github.com/JohannesBuchner/imagehash>"""
    img = Image.open(fname)
    hash = imagehash.whash(img, hash_size=HASH_SIZE).hash.flatten()

    # faiss requires float32
    return hash.astype('float32')


def search(img, idx, top_n=3):
    hash = imagehash.whash(img, hash_size=HASH_SIZE).hash.flatten()[None, ...].astype('float32')
    dists, ids = idx.search(hash, top_n)
    return dists, ids


if __name__ == '__main__':
    from flask import Flask, request, jsonify
    from data import fnames, mids

    print('preparing index...')
    idx = create_index(fnames, mids)

    print('starting server...')
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def query():
        data = request.get_json()
        img = np.array(data['image']).astype('uint8')
        img = Image.fromarray(img)
        dists, ids = search(img, idx)
        return jsonify(results=[
            {'id': id, 'dist': d} for id, d, in zip(ids, dists)])

    app.run(port=8888)