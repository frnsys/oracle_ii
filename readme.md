A simple MTG card scanner and catalog searcher

![](demo.gif)

## Scanner

### Setup

- Change into the `scanner` directory and install the requirements: `pip install -r requirements.txt`.
- Download `AllSets.json` from [mtgjson.com](http://mtgjson.com/) to `data/AllSets.json`.
- Run `python download.py` to download lo-res images from `gatherer.wizards.com`. This takes ~20-30min.
- Plug-in a commodity USB webcam and set it up so that it's pointing down.
- Calibrate the scanner in `detect.py`.
- Run `python scanner.py search` to start the search server. The search server runs separately so you only need to load the image hashes once.
- Run `python scanner.py` to start the scanner.
- Press `s` or `spacebar` when a card is in view and highlighted with a red border. This saves the card's multiverse id to a text file (`data/collection.db`).

The `lookup.py` script also lets you specify a card list and get their multiverse ids:

    python lookup.py cardlist

Where `cardlist` is a file with contents in the format:

    Card Name [quantity]

The quantity part is optional if it's just one card.

### Caveats

- The scanner is very sensitive to light conditions. You will likely have to calibrate it for your environment.
- It's recommended you use a light background, e.g. a piece of printer paper. The downside is that white-bordered cards will be tricky to scan.
- Has some trouble with foils, but ok for the most part.
- Has trouble with cards in sleeves, but this varies depending on sleeve color (darker sleeves do better).
- Search right now is just a brute-force through all MTG cards. On my netbook this search takes ~3 sec.
- This is not guaranteed to match the set of a card, though if the card has used different art for different sets, then it's a good bet it will match the set.
- Error rate is about ~2% (25 misses on a collection of 1045 cards).

The error rate likely could be improved by increasing the `HASH_SIZE` in `search.py`. If you do that, you'll want to increase the `max_distance` value in `main.py` as well.

## Catalog

### Running

- Once you've catalogued your cards, you can run the API with `python catalog.py`.
- Then visit `localhost:5000`.

### Updating prices

Prices are fetched from the `scryfall.com` API. You manually run `prices.py` to generate `data/prices.json`, which fetches prices for the cards in your collection. If you want to update the prices, you must manually do so by running this script again.

### Search syntax

Operators:

- `c:u` search for cards with `u` in the cost
- `c!g` search for cards without `g` in the cost
- `p>1` search for cards worth more than $1
- `p<1` search for cards worth less than $1
- logical operators for these are ok, e.g.
    - `c:u | c!g` searches for cards with blue _or_ without green
    - `c:u & c!g` searches for cards with blue _and_ without green
    - if an operator is absent, it's assumed to be `or`
    - you can group boolean operations with parentheses

Filters:

- `c` for color
- `t` for type
- `x` for text
- `p` for price
