"""
fetch prices for collection
"""

import json
import requests
from tqdm import tqdm
from time import sleep
from data import collection
from datetime import datetime

prices = {}
for mid in tqdm(collection.keys()):
    resp = requests.get('https://api.scryfall.com/cards/multiverse/{}'.format(mid))
    data = resp.json()
    prices[mid] = data.get('usd', None)
    sleep(0.01)

with open('data/prices.json', 'w') as f:
    json.dump({
        'prices': prices,
        'last_updated': datetime.now().timestamp()
    }, f)