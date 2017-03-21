import json
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
