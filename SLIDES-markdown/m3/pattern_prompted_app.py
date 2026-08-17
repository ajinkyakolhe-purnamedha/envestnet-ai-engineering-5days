"""Pattern 2: a prompted application returns a validated Python object."""

import os
from typing import Literal

import instructor
from google import genai
from pydantic import BaseModel, Field


class TradeIntent(BaseModel):
    action: Literal["buy", "sell"]
    symbol: str = Field(description="Uppercase stock ticker")
    shares: int = Field(gt=0, description="Whole shares requested")
    client: str


def extract_trade(note: str, client: instructor.Instructor) -> TradeIntent:
    """Turn an advisor note into typed application data, not prose."""
    return client.create(
        response_model=TradeIntent,
        messages=[{"role": "user", "content": f"Extract the trade: {note}"}],
    )


def validate_trade_intent(intent: TradeIntent) -> bool:
    """Business validation remains application code, not model output."""
    return intent.symbol in {"AAPL", "SPY", "QQQ"}


if __name__ == "__main__":
    if api_key := os.getenv("GEMINI_API_KEY"):
        structured_client = instructor.from_genai(genai.Client(api_key=api_key))
        trade = extract_trade("Buy 10 shares of AAPL for Alice.", structured_client)
        print(trade)
        print("Allowed symbol:", validate_trade_intent(trade))
    else:
        print("Set GEMINI_API_KEY in .env to run the extraction.")
