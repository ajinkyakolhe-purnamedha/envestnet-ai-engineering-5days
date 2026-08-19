"""Vector search cannot add up. SQL can."""

import sqlite3

import pandas as pd
from pydantic import BaseModel, Field, field_validator

from chronos_offline import DATA

conn = sqlite3.connect(":memory:")
prices = pd.read_csv(DATA / "prices.csv")
prices.to_sql("prices", conn, index=False)

SIMULATED_DATE = "2020-06-01"


# #region governed
class PriceQuery(BaseModel):
    """The model fills this in. It never writes SQL."""

    symbol: str = Field(pattern=r"^[A-Z]{1,5}$")
    trading_days: int = Field(ge=1, le=90)

    @field_validator("symbol")
    @classmethod
    def known_symbol(cls, v: str) -> str:
        allowed = {"AAPL", "MSFT", "SPY", "GLD", "JPM"}
        if v not in allowed:
            raise ValueError(f"{v} is not a curated symbol")
        return v


def average_close(query: PriceQuery, as_of: str) -> float:
    """One reviewed statement. Parameters, never f-strings."""
    rows = conn.execute(
        "SELECT AVG(close) FROM ("
        "  SELECT close FROM prices"
        "  WHERE symbol = ? AND date <= ?"
        "  ORDER BY date DESC LIMIT ?)",
        (query.symbol, as_of, query.trading_days),
    )
    return round(list(rows)[0][0], 2)
# #endregion governed


ask = PriceQuery(symbol="AAPL", trading_days=30)
print(ask.symbol, average_close(ask, SIMULATED_DATE))

try:
    PriceQuery(symbol="DROP", trading_days=30)
except ValueError as error:
    print("rejected:", error.errors()[0]["ctx"]["error"])

# The model chose a symbol and a window. It did not choose
# the table, the columns, the date filter, or the LIMIT.
#
# That `date <= ?` is the point-in-time rule, enforced in
# the one place the model cannot reach. Free-form
# text-to-SQL would let it write `date <= '2021-12-31'`
# and quietly show the investor the future.
