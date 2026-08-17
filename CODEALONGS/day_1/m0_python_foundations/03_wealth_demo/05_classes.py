from dataclasses import dataclass


@dataclass
class Holding:
    symbol: str
    shares: int
    purchase_price: float

    def market_value(self, latest_price: float) -> float:
        """Return this holding's current market value."""
        return self.shares * latest_price


holding = Holding("AAPL", 10, 80.50)
print(f"{holding.symbol} market value: {holding.market_value(82.50)}")
