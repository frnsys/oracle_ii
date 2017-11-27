A simple MTG card scanner

## Setup

- Install the requirements: `pip install -r requirements.txt`
- Download `AllSets.json` from [mtgjson.com](http://mtgjson.com/).
- Run `python download.py` to download lo-res images from `gatherer.wizards.com`. This takes ~20-30min.
- Plug-in a commodity USB webcam and set it up so that it's pointing down.
- Calibrate the scanner in `detect.py`.
- Run `python search.py` to start the search server. The search server runs separately so you only need to load the image hashes once.
- Run `python main.py` to start the scanner.
- Press `s` or `spacebar` when a card is in view and highlighted with a red border. This saves the card's multiverse id to a text file (`data/collection.db`).

The `lookup.py` script also lets you specify a card list and get their multiverse ids:

    python lookup.py cardlist

Where `cardlist` contains contents in the format:

    Card Name [quantity]

The quantity part is optional if it's just one card.

## Running the catalog API

- Once you've catalogued your cards, you can run the API with `python api.py`.
- There's a demo page at `catalog/index.html`.

## Caveats

- The scanner is very sensitive to light conditions. You will likely have to calibrate it for your environment.
- It's recommended you use a light background, e.g. a piece of printer paper. The downside is that white-bordered cards will be tricky to scan.
- Has some trouble with foils, but ok for the most part.
- Has trouble with cards in sleeves, but this varies depending on sleeve color (darker sleeves do better).
- Search right now is just a brute-force through all MTG cards. On my netbook this search takes ~3 sec.
- This is not guaranteed to match the set of a card, though if the card has used different art for different sets, then it's a good bet it will match the set.
- Error rate is about ~2% (25 misses on a collection of 1045 cards).

The error rate likely could be improved by increasing the `HASH_SIZE` in `search.py`. If you do that, you'll want to increase the `max_distance` value in `main.py` as well.
