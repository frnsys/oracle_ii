import os
import requests
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
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


def run_parallel(arr, fn, n_jobs=8, use_kwargs=False):
    if n_jobs==1:
        return [fn(**a) if use_kwargs else fn(a) for a in tqdm(arr)]
    #Assemble the workers
    with ProcessPoolExecutor(max_workers=n_jobs) as pool:
        #Pass the elements of array into function
        if use_kwargs:
            futures = [pool.submit(fn, **a) for a in arr]
        else:
            futures = [pool.submit(fn, a) for a in arr]
        kwargs = {
            'total': len(futures),
            'unit': 'it',
            'unit_scale': True,
            'leave': True
        }
        #Print out the progress as tasks complete
        for f in tqdm(as_completed(futures), **kwargs):
            pass
    out = []
    #Get the results from the futures.
    for i, future in tqdm(enumerate(futures)):
        try:
            out.append(future.result())
        except Exception as e:
            out.append(e)
    return out


if __name__ == '__main__':
    downloaded = [f.replace('.jpg', '') for f in os.listdir('imgs')]

    to_download = []
    for mid, card in cards.items():
        if keep(card) and mid not in downloaded:
            to_download.append(card)
    print('REMAINING:', len(to_download))

    run_parallel(to_download, download)
