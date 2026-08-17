"""One concept: describe the response shape with Instructor plus Pydantic."""

from typing import Literal

import instructor
from pydantic import BaseModel, Field


class TradeIntent(BaseModel):
    action: Literal["buy", "sell"]
    symbol: str
    shares: int = Field(gt=0)


def extract_trade(client: instructor.Instructor, note: str) -> TradeIntent:
    """Ask an injected Instructor client for a typed trade intent."""
    return client.create(
        response_model=TradeIntent,
        messages=[{"role": "user", "content": note}],
    )
