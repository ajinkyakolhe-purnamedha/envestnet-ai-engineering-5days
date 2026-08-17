def purchase_cost(shares: int, price: float) -> float:
    """Return the cost of buying shares at a price."""
    if shares <= 0 or price <= 0:
        raise ValueError("Shares and price must be positive.")
    return shares * price


print(f"Purchase cost: {purchase_cost(10, 80.50)}")
