"""The Chronos Wealth backend.

Run:
    uv run --project ../CODE-ALONGS \
        uvicorn m0.api_server:api --reload

Type hints become validation, docs, and the API contract.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

api = FastAPI(title="Chronos Wealth")


# #region api
class Holding(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    shares: float = Field(gt=0)         # rejected at the edge
    average_cost: float = Field(gt=0)
    risk_level: str = "MEDIUM"


BOOK: dict[str, Holding] = {}


@api.post("/holdings")
def add_holding(holding: Holding) -> Holding:
    """Pydantic already validated it. Nothing to check."""
    BOOK[holding.symbol] = holding
    return holding


@api.get("/holdings/{symbol}")
def get_holding(symbol: str) -> Holding:
    if symbol not in BOOK:
        raise HTTPException(404, f"no holding {symbol}")
    return BOOK[symbol]
# #endregion api


# uv run --project ../CODE-ALONGS uvicorn m0.api_server:api --reload
# -> http://localhost:8000/docs
