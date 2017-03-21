def diff(a, b):
    a_keys, b_keys, = a.types.keys(), b.types.keys()
    additions = [
        '<{}: {}>'.format(k, b.types[k])
        for k in b_keys - a_keys
    ]
    deletions = [
        '<{}: {}>'.format(k, a.types[k])
        for k in a_keys - b_keys
    ]
    changes = [
        '<{}: {} != {}>'.format(
            k, a.types[k], b.types[k]
        )
        for k in a_keys & b_keys
        if a.types[k] != b.types[k]
    ]

    return {
        '+': additions,
        '-': deletions,
        '~': changes
    }
