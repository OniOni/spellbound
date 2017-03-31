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


class NoneType(JsonType):
    __type__ = 'null'


    def __repr__(self):
        return '<null>'


class ListType(JsonType):
    __type__ = 'list'

    def __init__(self, lst=None):
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

    def __init__(self, dct=None):
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
