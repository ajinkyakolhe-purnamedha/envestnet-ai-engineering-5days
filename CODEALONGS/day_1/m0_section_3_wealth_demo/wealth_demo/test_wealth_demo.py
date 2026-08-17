"""Standard-library tests participants can run without pytest knowledge."""

import sqlite3
import unittest

from wealth_demo.calculations import gain_loss, purchase_cost
from wealth_demo.models import Holding, Portfolio
from wealth_demo.storage import create_database, get_price_as_of, load_holdings, save_holding, seed_prices


class WealthDemoTests(unittest.TestCase):
    def test_calculations(self) -> None:
        self.assertEqual(purchase_cost(10, 80.50), 805.0)
        self.assertEqual(gain_loss(805.0, 850.0), 45.0)

    def test_insufficient_cash_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "cash"):
            Portfolio(cash=100.0).buy(Holding("AAPL", 10, 80.50))

    def test_storage_round_trip_and_point_in_time_lookup(self) -> None:
        connection = sqlite3.connect(":memory:")
        create_database(connection)
        seed_prices(connection)
        holding = Holding("AAPL", 10, 80.50)
        save_holding(connection, holding)
        self.assertEqual(load_holdings(connection), [holding])
        self.assertEqual(get_price_as_of(connection, "AAPL", "2020-06-01"), 80.46)


if __name__ == "__main__":
    unittest.main()
