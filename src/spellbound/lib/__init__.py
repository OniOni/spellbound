import json

from spellbound.lib.types import *

def to_type(doc, collection=None):
    if collection is None:
        collection = {}

    if isinstance(doc, str):
        t = StringType()
    elif isinstance(doc, int):
        t =  IntType()
    elif isinstance(doc, dict):
        t = DictType(doc)
        for key, d in doc.items():
            st, collection = to_type(d, collection)
            t.add(key, st)
    elif isinstance(doc, list):
        t = ListType(doc)
        for d in doc:
            st, collection = to_type(d, collection)
            t.add(st)
    elif isinstance(doc, type(None)):
        t = NoneType()
    else:
        raise TypeError("Can't process: %s", type(doc))

    if t not in collection:
        collection[t] = 1
    else:
        collection[t] += 1

    return t, collection


def parse(string):
    doc = json.loads(string)
    doc, _ = to_type(doc)
    return doc


def _loads(doc):
    if doc['type'] == 'string':
        t = StringType()
    elif doc['type'] == 'number':
        t =  IntType()
    elif doc['type'] == 'object':
        t = DictType()
        for key, d in doc['properties'].items():
            st = _loads(d)
            t.add(key, st)
    elif doc['type'] == 'list':
        t = ListType()
        for d in doc['items']:
            st = _loads(d)
            t.add(st)
    elif doc['type'] == 'null':
        t = NoneType()
    else:
        raise TypeError("Can't process: %s", doc['type'])

    return t

def loads(string):
    doc = json.loads(string)
    return _loads(doc)

def dumps(doc):
    return json.dumps(doc.schema())
