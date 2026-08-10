# Pydantic validation
from pydantic import BaseModel, PositiveFloat

class Trade(BaseModel):
    symbol: str
    amount: PositiveFloat

trade = Trade(symbol="SPY", amount=1_000)
print(trade)

