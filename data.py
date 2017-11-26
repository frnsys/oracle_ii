"""
loads card data
"""

import os
import json

data = json.load(open('AllSets.json', 'r'))

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
