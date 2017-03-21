import argparse
import sys

from spellbound.lib import parse, dumps


def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, default=None)

    return parser.parse_args()

def run(args):
    _input = sys.stdin.read()
    if args.s:
        print('Diff')
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
