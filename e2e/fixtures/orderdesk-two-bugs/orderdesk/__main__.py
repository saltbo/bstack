import sys

from .store import ORDERS, page, revenue


def main(argv):
    if argv[:1] == ["revenue"]:
        print(revenue(ORDERS))
        return 0
    if argv[:1] != ["list"]:
        print("usage: python3 -m orderdesk list | revenue", file=sys.stderr)
        return 2
    cursor = None
    while True:
        items, cursor = page(ORDERS, after=cursor)
        for order in items:
            print(f"{order.id}\t{order.created_at}\t{order.total}")
        if cursor is None:
            return 0


sys.exit(main(sys.argv[1:]))
