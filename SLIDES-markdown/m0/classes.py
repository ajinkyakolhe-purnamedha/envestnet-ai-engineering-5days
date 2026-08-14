"""Classes: the shape of your domain, expressed once.

Run:
    uv run --project ../CODE-ALONGS \
        python m0/classes.py
"""

from dataclasses import dataclass


# #region shapes
@dataclass
class Holding:
    symbol: str
    shares: float
    close: float

    @property
    def market_value(self) -> float:
        return self.shares * self.close


class Portfolio:
    def __init__(self, cash_balance: float) -> None:
        self._cash = cash_balance
        self._holdings: list[Holding] = []

    def add(self, holding: Holding) -> None:
        self._holdings.append(holding)

    @property
    def total_value(self) -> float:
        held = sum(h.market_value for h in self._holdings)
        return self._cash + held
# #endregion shapes


book = Portfolio(cash_balance=100_000.0)
book.add(Holding("AAPL", shares=100, close=80.46))
book.add(Holding("MSFT", shares=150, close=182.83))
print(f"Total value: {book.total_value:,.2f}")

# Lesson:
# - dataclass is good for simple records.
# - class is good when the object owns behavior.
