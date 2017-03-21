import json

def load(doc, collection=None):
    if collection is None:
        collection = {}

    if isinstance(doc, str):
        t = StringType()
    elif isinstance(doc, int):
        t =  IntType()
    elif isinstance(doc, dict):
        t = DictType(doc)
        for key, d in doc.items():
            st, collection = load(d, collection)
            t.add(key, st)
    elif isinstance(doc, list):
        t = ListType(doc)
        for d in doc:
            st, collection = load(d, collection)
            t.add(st)
    else:
        raise TypeError("Can't process: %s", type(doc))

    if t not in collection:
        collection[t] = 1
    else:
        collection[t] += 1

    return t, collection


def loads(string):
    doc = json.loads(string)
    doc, _ = load()
    return doc

def dumps(doc):
    return json.dumps(doc.schema())
