"""
parses a search query
and searches cards

supports:

- searching title text:
    - can be a single unquoted word
    - if using multiple words, must put in double quotes
- searching by colors in cost:
    - `c:g` searches for green in the mana cost
    - `c!g` searches for anything without green in the mana cost
- searching by type:
    - `t:artifact` searches for artifact in type
    - `t!artifact` searches for artifact not in type
- searching in text:
    - `x:counter` searches for "counter" in text
    - `x!counter` searches for "counter" not in text
    - if using multiple words, use double quotes, e.g. `x:"destroy target"`
- searching by price:
    - `p>1` searchs for cards worth more than $1

any of the above can be combined with boolean operators.
if using multiple, you __must__ combine them with boolean operators, e.g.

    "ancestry" & (c:u | c:b)

"""

import operator
from pyparsing import Literal, Word, ZeroOrMore, Forward, alphanums, oneOf, Group, ParseResults, QuotedString

KEYMAP = {
    'c': 'manaCost', # todo this maybe should be color identity?
    'x': 'text',
    't': 'type',
    'p': 'price'
}

OPS = {
    '<': operator.lt,
    '>': operator.gt
}


def Syntax():
    expr = Forward()

    # operators
    bool_op = oneOf('& |')
    contain_op = oneOf(': ! < >')

    # e.g. `c:w` or `c!w` or `t:artifact` or `x:"destroy target creature"`
    filter = Group(Word(alphanums, exact=1) + contain_op + (Word(alphanums) | QuotedString(quoteChar='"')))

    # parentheses
    lpar = Literal('(').suppress()
    rpar = Literal(')').suppress()

    # handle:
    # - filters (see above)
    # - single unquoted words
    # - multiple quoted words
    # - any of the above in parentheses with boolean operators
    atom = filter | Word(alphanums) | QuotedString(quoteChar='"') | Group(lpar + expr + rpar)
    expr << atom + ZeroOrMore(bool_op + expr)
    return expr


def ltr_triplets(s, n=3):
    """takes a list of symbols and
    recursively ensures that they are in triplets"""
    s = [ltr_triplets(list(p)) if isinstance(p, ParseResults) else p for p in s]
    if len(s) > n:
        s = s[:-n] + [s[-n:]]
        return ltr_triplets(s)
    return s


def make_predicate(q):
    """create predicates from a query unit,
    i.e. a quoted string or a triplet of [a, :!, b]"""
    if isinstance(q, list):
        type, op, q = q
        key = KEYMAP[type]
        if op in [':', '!']:
            q = q.lower()
            pos = op == ':'
            return lambda c: (q in c.get(key, '').lower()) == pos
        elif op in ['<', '>']:
            q = float(q)
            return lambda c: OPS[op](float(c.get(key) or 0), q)
    else:
        q = q.lower()
        return lambda c: q in c['name'].lower()


def make_predicates(parts):
    """take a parsed query and turn it
    into a nested predicate"""

    # handle regular strings
    if len(parts) == 1:
        return make_predicate(parts[0])
    elif isinstance(parts, str):
        return make_predicate(parts)

    # check that this is a predicate triplet
    elif parts[1] in [':', '!']:
        return make_predicate(parts)

    # handle boolean operators for predicate pairs
    else:
        op = parts[1]
        a, b = make_predicates(parts[0]), make_predicates(parts[-1])
        if op == '&':
            return lambda c: a(c) and b(c)
        else:
            return lambda c: a(c) or b(c)

def parse_query(query):
    """parses a search query into a predicate"""
    expr = Syntax()
    parts = expr.parseString(query)
    parts = ltr_triplets(parts)
    return make_predicates(parts)
