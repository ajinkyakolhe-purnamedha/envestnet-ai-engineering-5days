"""Holding and portfolio domain objects."""

from dataclasses import dataclass, field

from wealth_demo.calculations import current_value, purchase_cost


@dataclass
class Holding:
    """One purchased security."""

    symbol: str
    shares: int
    purchase_price: float

    def market_value(self, latest_price: float) -> float:
        """Return this holding's current market value."""
        return current_value(self.shares, latest_price)


@dataclass
class Portfolio:
    """Cash and purchased holdings."""

    cash: float
    holdings: list[Holding] = field(default_factory=list)

    def buy(self, holding: Holding) -> None:
        """Buy a holding when the portfolio has enough cash."""
        cost = purchase_cost(holding.shares, holding.purchase_price)
        if cost > self.cash:
            raise ValueError("Not enough cash to buy this holding.")
        self.cash -= cost
        self.holdings.append(holding)

    def total_value(self, latest_prices: dict[str, float]) -> float:
        """Return cash plus the market value of every holding."""
        return self.cash + sum(
            holding.market_value(latest_prices[holding.symbol])
            for holding in self.holdings
        )
