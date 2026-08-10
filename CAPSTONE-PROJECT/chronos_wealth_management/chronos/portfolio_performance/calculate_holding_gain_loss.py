"""Pure arithmetic for holding valuation — no database access."""


def calculate_holding_market_value(shares: float, current_price: float) -> float:
    return shares * current_price


def calculate_holding_cost_basis(shares: float, average_cost: float) -> float:
    return shares * average_cost


def calculate_unrealized_gain_loss(market_value: float, cost_basis: float) -> float:
    return market_value - cost_basis
