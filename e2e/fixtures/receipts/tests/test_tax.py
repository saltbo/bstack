import unittest

from receipts import with_tax


class TaxTest(unittest.TestCase):
    def test_no_tax(self):
        self.assertEqual(1000, with_tax(1000, 0))


if __name__ == "__main__":
    unittest.main()
