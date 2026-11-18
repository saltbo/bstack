import unittest

from orderdesk import Order, page


class PageTest(unittest.TestCase):
    def test_first_page_is_oldest_first(self):
        orders = [Order(2, 20, 1), Order(1, 10, 1), Order(3, 30, 1)]
        items, cursor = page(orders, limit=2)
        self.assertEqual([1, 2], [o.id for o in items])
        self.assertIsNotNone(cursor)


if __name__ == "__main__":
    unittest.main()
