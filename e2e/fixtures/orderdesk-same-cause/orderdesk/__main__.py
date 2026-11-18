import sys

from .store import ORDERS, page


def all_orders():
    cursor = None
    while True:
        items, cursor = page(ORDERS, after=cursor)
        yield from items
        if cursor is None:
            return


def main(argv):
    if argv[:1] == ["list"]:
        for order in all_orders():
            print(f"{order.id}\t{order.created_at}\t{order.total}")
        return 0
    if argv[:1] == ["export"]:
        print("id,created_at,total")
        for order in all_orders():
            print(f"{order.id},{order.created_at},{order.total}")
        return 0
    print("usage: python3 -m orderdesk <command>", file=sys.stderr)
    return 2


sys.exit(main(sys.argv[1:]))
