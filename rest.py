class JsonType(object):

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, b):
        return hash(self) == hash(b)


class IntType(JsonType):

    def __repr__(self):
        return '<int>'

class StringType(JsonType):

    def __repr__(self):
        return '<str>'

class ListType(JsonType):

    def __init__(self, lst):
        self.types = set([
            type_of(d)
            for d in lst
        ])

    def __repr__(self):
        return '<list [{}]>'.format(
            "|".join([repr(t) for t in self.types])
        )


class DictType(JsonType):

    def __init__(self, dct):
        self.types = {
            k: type_of(v)
            for k, v in dct.items()
        }

    def __repr__(self):
        return '<dict ({})>'.format(", ".join([
            '{}: {}'.format(k, v)
            for k, v in self.types.items()
        ]))


def type_of(doc):
    if isinstance(doc, str):
        return StringType()
    elif isinstance(doc, int):
        return IntType()
    elif isinstance(doc, dict):
        return DictType(doc)
    elif isinstance(doc, list):
        return ListType(doc)
    else:
        raise TypeError("Can't process: %s", type(doc))


if __name__ == '__main__':
    print(type_of({
        'k': 42,
        'l': [1,2,3, 'hey'],
        's': 'hello',
        'd': {
            'k2': 42,
            'l': [{'k': 42}, {'k': 100}]
        }
    }))

    print(type_of([1,2,3, 'hey']))
