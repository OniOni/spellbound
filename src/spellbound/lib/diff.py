from spellbound.lib.types import DictType

def dict_diff(a, b):
    a_keys, b_keys, = a.types.keys(), b.types.keys()
    additions = [
        '<{}: {}>'.format(k, b.types[k])
        for k in b_keys - a_keys
    ]
    deletions = [
        '<{}: {}>'.format(k, a.types[k])
        for k in a_keys - b_keys
    ]
    changes = {
        k: diff(a.types[k], b.types[k])
        for k in a_keys & b_keys
        if a.types[k] != b.types[k]
    }

    return {
        '+': additions,
        '-': deletions,
        '~': changes
    }

def diff(a, b):
    if isinstance(a, DictType) and isinstance(b, DictType):
        return dict_diff(a, b)
    else:
        return {
            'expected': str(a),
            'actual': str(b)
        }
