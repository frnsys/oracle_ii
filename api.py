"""
serves a simple API for getting the saved catalog
"""

from db import DB
from data import cards
from flask_cors import CORS
from flask import Flask, jsonify

db = DB('collection.db')
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    collection = {}
    for mid in db.all():
        if mid not in collection:
            collection[mid] = cards[mid]
            collection[mid]['quantity'] = 1
        else:
            collection[mid]['quantity'] += 1
    return jsonify(cards=collection)


if __name__ == '__main__':
    app.run()