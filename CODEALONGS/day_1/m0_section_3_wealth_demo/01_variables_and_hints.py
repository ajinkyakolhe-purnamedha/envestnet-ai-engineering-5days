symbol: str = "AAPL"
shares: int = 10
purchase_price: float = 80.50

purchase_cost: float = shares * purchase_price
print(f"{symbol} purchase cost: {purchase_cost}")
