"""
catalog app
"""

import json
from catalog.parser import parse_query
from flask_cors import CORS
from flask import Flask, render_template, send_from_directory, jsonify, request

app = Flask(__name__)
CORS(app)
collection = json.load(open('data/collection.json', 'r'))


@app.route('/')
def index():
    return render_template('index.html', cards=collection.values())


@app.route('/img/<id>')
def image(id):
    return send_from_directory('../imgs', '{}.jpg'.format(id))


@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    if not query:
        results = []
    else:
        pred = parse_query(query)
        results = [c['multiverseid'] for c in filter(pred, collection.values())]
    return jsonify(results=results)