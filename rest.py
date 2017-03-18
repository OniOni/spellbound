class JsonType(object):

    def _format_subtypes(self):
        return None

    def __repr__(self):
        return '<{} {}>'.format(
            self.__type__,
            self._format_subtypes()
        )

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, b):
        return hash(self) == hash(b)


class IntType(JsonType):
    __type__ = 'number'

    def __repr__(self):
        return '<int>'


class StringType(JsonType):
    __type__ = 'string'

    def __repr__(self):
        return '<str>'


class ListType(JsonType):
    __type__ = 'list'

    def __init__(self, lst):
        self.types = set()

    def add(self, type):
        self.types.add(type)

    def _format_subtypes(self):
        return '[{}]'.format(
            "|".join([repr(t) for t in self.types])
        )


class DictType(JsonType):
    __type__ = 'map'

    def __init__(self, dct):
        self.types = {}

    def add(self, key, type):
        self.types[key] = type

    def _format_subtypes(self):
        return '({})'.format(", ".join([
            '{}: {}'.format(k, v)
            for k, v in self.types.items()
        ]))

def type_of(doc, collection=None):
    if collection is None:
        collection = {}

    if isinstance(doc, str):
        t = StringType()
    elif isinstance(doc, int):
        t =  IntType()
    elif isinstance(doc, dict):
        t = DictType(doc)
        for key, d in doc.items():
            st, collection = type_of(d, collection)
            t.add(key, st)
    elif isinstance(doc, list):
        t = ListType(doc)
        for d in doc:
            st, collection = type_of(d, collection)
            t.add(st)
    else:
        raise TypeError("Can't process: %s", type(doc))

    if t not in collection:
        collection[t] = 1
    else:
        collection[t] += 1

    return t, collection

def diff(a, b, strict=True):

    if strict:
        return a == b



if __name__ == '__main__':
    tree, types = type_of({
        'k': 42,
        'l': [1,2,3, 'hey'],
        's': 'hello',
        'd': {
            'k2': 42,
            'l': [{'k': 42}, {'k': 100}]
        }
    })
    print('Tree: ', tree)
    print('Types: ', types)


    tree, types = type_of([1,2,3, 'hey'])
    print('Tree: ', tree)
    print('Types: ', types)
