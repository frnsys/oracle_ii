"""
get multiverse id for a card by name
"""

from data import cards


def lookup(name):
    """returns the first multiverse id
    matching a card name (i.e. ignores sets)"""
    for mid, card in cards.items():
        if card['name'] == name:
            return mid


def cardlist_to_mids(cardlist):
    """converts a file with cardnames
    formatted with an optional quantity after
    (in the format `[n]` following the card name)
    to a list of multiverse ids"""
    cards = []
    raw = open(cardlist, 'r').readlines()
    for l in raw:
        l = l.strip()
        if not l:
            continue
        parts = l.split('[')
        name = parts[0].strip()
        if len(parts) > 1:
            quantity = int(parts[1][:-1])
        else:
            quantity = 1
        mid = lookup(name)
        if mid is None:
            raise Exception('No card found for "{}"'.format(name))
        for _ in range(quantity):
            cards.append(mid)
    return cards


if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    mids = cardlist_to_mids(fname)
    for mid in mids:
        print(mid)