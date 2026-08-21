"""One concept: describe the response shape with Instructor plus Pydantic.

Try:
- Change shares to 0 and inspect the schema error.
- Add allocation_percent=36 and ask whether the schema knows policy.
- Keep business validation in Python, outside the LLM response schema.
"""

from typing import Literal

import instructor
from pydantic import BaseModel, Field, ValidationError

from m3_smolm_setup import call_smolm


class TradeIntent(BaseModel):
    action: Literal["buy", "sell"]
    symbol: str
    shares: int = Field(gt=0)


def extract_trade(client: instructor.Instructor, note: str) -> TradeIntent:
    return client.create(response_model=TradeIntent, messages=[{"role": "user", "content": note}])


def validate_trade_intent(intent: TradeIntent, allocation_percent: float) -> bool:
    return intent.symbol in {"AAPL", "SPY", "QQQ"} and allocation_percent <= 35


messages = [
    {"role": "system", "content": "Extract trade intent as JSON: action, symbol, shares."},
    {"role": "user", "content": "Please buy 150 shares of AAPL."},
]
raw_reply = call_smolm(messages)

valid_intent = TradeIntent(action="buy", symbol="AAPL", shares=150)
try:
    TradeIntent(action="buy", symbol="SPY", shares=0)
except ValidationError as error:
    schema_error = error.errors()[0]["msg"]

print("typed intent:", valid_intent)
print("raw model text:", raw_reply)
print("schema error:", schema_error)
print("business allowed:", validate_trade_intent(valid_intent, allocation_percent=35))
print("business rejected:", validate_trade_intent(valid_intent, allocation_percent=36))
