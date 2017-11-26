"""
for downloading lo-res images from gatherer.
"""

import os
import requests
import util
from data import cards

BASE_URL = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={}&type=card'


def keep(card):
    """predicate for whether or not to keep a card"""
    return card['rarity'] != 'Basic Land'


def download(card):
    mid = card['multiverseid']
    download_image(BASE_URL.format(mid), 'imgs/{}.jpg'.format(mid))


def download_image(url, path):
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in res:
                f.write(chunk)
    else:
        print('failed to download:', url)
        # res.raise_for_status()


if __name__ == '__main__':
    downloaded = [f.replace('.jpg', '') for f in os.listdir('imgs')]

    to_download = []
    for mid, card in cards.items():
        if keep(card) and mid not in downloaded:
            to_download.append(card)
    print('REMAINING:', len(to_download))

    util.run_parallel(to_download, download)
