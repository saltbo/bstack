import sys

from .tax import with_tax

RATE = 0.08


def main(argv):
    if argv[:1] == ["total"] and len(argv) == 2:
        print(with_tax(int(argv[1]), RATE))
        return 0
    print("usage: python3 -m receipts total <cents>", file=sys.stderr)
    return 2


sys.exit(main(sys.argv[1:]))
