def type_of(doc):
    if isinstance(doc, basestring):
        return '<str>'
    elif isinstance(doc, int):
        return '<int>'
    elif isinstance(doc, dict):

        return '<dict {}{}{}>'.format('{', ",".join([
            '{}: {}'.format(k, type_of(v))
            for k, v in doc.items()
        ]), '}')
    elif isinstance(doc, list):
        return '<list [{}]>'.format('|'.join(set([
            type_of(d)
            for d in doc
        ])))
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
