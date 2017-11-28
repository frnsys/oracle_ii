"""
loads card data
"""

import os
import json
from db import DB

db = DB('collection.db')
data = json.load(open('AllSets.json', 'r'))
prices = json.load(open('data/prices.json', 'r'))

# map multiverse id to card data
cards = {}
for set_name, set in data.items():
    for c in set['cards']:
        mid = c.get('multiverseid')
        if mid is None:
            continue
        cards[mid] = c


downloaded = os.listdir('imgs')
fnames, mids = [], []
for mid, card in cards.items():
    fname = '{}.jpg'.format(mid)
    if fname not in downloaded:
        continue
    fnames.append(os.path.join('imgs', fname))
    mids.append(mid)


collection = {}
for mid in db.all():
    if mid not in collection:
        collection[mid] = cards[mid]
        collection[mid]['quantity'] = 1
        collection[mid]['price'] = prices['prices'].get(str(mid))
    else:
        collection[mid]['quantity'] += 1
