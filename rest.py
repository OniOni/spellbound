import json

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

    def schema(self):
        return {
            'type': self.__type__
        }


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

    def schema(self):
        schema = super().schema()
        schema.update({
            'items': [
                i.schema()
                for i in self.types
            ]
        })

        return schema

class DictType(JsonType):
    __type__ = 'object'

    def __init__(self, dct):
        self.types = {}

    def add(self, key, type):
        self.types[key] = type

    def _format_subtypes(self):
        return '({})'.format(", ".join([
            '{}: {}'.format(k, v)
            for k, v in self.types.items()
        ]))

    def schema(self):
        schema = super().schema()
        schema.update({
            'properties': {
                k: v.schema()
                for k, v in self.types.items()
            }
        })

        return schema

    def diff(self, b):
        a_keys, b_keys, = self.types.keys(), b.types.keys()
        additions = [
            '<{}: {}>'.format(k, b.types[k])
            for k in b_keys - a_keys
        ]
        deletions = [
            '<{}: {}>'.format(k, self.types[k])
            for k in a_keys - b_keys
        ]
        changes = [
            '<{}: {} != {}>'.format(
                k, self.types[k], b.types[k]
            )
            for k in a_keys & b_keys
            if self.types[k] != b.types[k]
        ]

        return {
            '+': additions,
            '-': deletions,
            '~': changes
        }

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
    schema = tree.schema()
    print(json.dumps(schema))
    # print('Tree: ', tree)
    # print('Types: ', types)
    # print('schema: ', schema)

    tree, types = type_of([1,2,3, 'hey'])
    # print('Tree: ', tree)
    # print('Types: ', types)

    obj1, _ = type_of({
        'k': 'hey',
        'k2': 42,
        'k4': 42
    })

    obj2, _ = type_of({
        'k': 'hey',
        'k3': 42,
        'k4': 'hey'
    })

    # print('Diff: ', obj1.diff(obj2))
