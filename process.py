import json
from db import DB
from data import cards

db = DB('collection.db')
prices = json.load(open('data/prices.json', 'r'))

collection = {}
for mid in db.all():
    if mid not in collection:
        collection[mid] = cards[mid]
        collection[mid]['quantity'] = 1
        collection[mid]['price'] = prices['prices'].get(str(mid))
    else:
        collection[mid]['quantity'] += 1

with open('data/collection.json', 'w') as f:
    json.dump(collection, f)
