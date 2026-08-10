# Dataclasses
from dataclasses import dataclass

@dataclass
class Holding:
    symbol: str
    shares: int

holding = Holding("SPY", 100)
print(holding)

