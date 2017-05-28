import argparse
import json
import sys

from spellbound.lib import parse, dumps, loads
from spellbound.lib.diff import diff

def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, default=None)

    return parser.parse_args()

def run(args):
    input_ = sys.stdin.read()
    if args.s:
        with open(args.s, 'r') as f:
            schema = f.read()

        a, b = loads(schema), parse(input_)
        d = diff(a, b)
        print(json.dumps(d))
    else:
        doc = parse(_input)
        print(dumps(doc))

def main():
    args = setup()
    run(args)


# curl test.com | spellbound > schema.json
# curl test.com | spellbound -s schema.json > diff.json
if __name__ == '__main__':
    main()
