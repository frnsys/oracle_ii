"""
catalog app
"""

from db import DB
from data import cards
from parser import parse_query
from flask_cors import CORS
from flask import Flask, render_template, send_from_directory, jsonify, request

db = DB('collection.db')
app = Flask(__name__)
CORS(app)

collection = {}
for mid in db.all():
    if mid not in collection:
        collection[mid] = cards[mid]
        collection[mid]['quantity'] = 1
    else:
        collection[mid]['quantity'] += 1


@app.route('/')
def index():
    return render_template('index.html', cards=collection.values())


@app.route('/img/<id>')
def image(id):
    return send_from_directory('imgs', '{}.jpg'.format(id))


@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    if not query:
        results = []
    else:
        pred = parse_query(query)
        results = [c['multiverseid'] for c in filter(pred, collection.values())]
    return jsonify(results=results)


if __name__ == '__main__':
    app.run(debug=True)