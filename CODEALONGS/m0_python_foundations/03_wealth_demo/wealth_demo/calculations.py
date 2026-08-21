"""Small, reusable wealth calculations."""


def purchase_cost(shares: int, price: float) -> float:
    """Return the cost of buying shares at a price."""
    if shares <= 0 or price <= 0:
        raise ValueError("Shares and price must be positive.")
    return shares * price


def current_value(shares: int, latest_price: float) -> float:
    """Return the current value of shares at the latest price."""
    if shares <= 0 or latest_price <= 0:
        raise ValueError("Shares and price must be positive.")
    return shares * latest_price


def gain_loss(cost: float, value: float) -> float:
    """Return the gain or loss relative to purchase cost."""
    return value - cost
