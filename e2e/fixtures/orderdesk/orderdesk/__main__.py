import sys

from .store import ORDERS, page


def main(argv):
    if argv[:1] != ["list"]:
        print("usage: python3 -m orderdesk list", file=sys.stderr)
        return 2
    cursor = None
    while True:
        items, cursor = page(ORDERS, after=cursor)
        for order in items:
            print(f"{order.id}\t{order.created_at}\t{order.total}")
        if cursor is None:
            return 0


sys.exit(main(sys.argv[1:]))
