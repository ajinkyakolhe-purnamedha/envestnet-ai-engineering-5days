"""Variables and type hints. A Chronos price row.

Run:
    uv run --project ../CODE-ALONGS \
        python m0/variables.py
"""

# Python infers types. You never declare them to run code.
symbol = "AAPL"
close = 80.46
is_tradable = True
tags = ["equity", "technology", "large-cap"]

# But you SHOULD annotate. Hints are documentation the
# IDE can check -- and what Pydantic/FastAPI use to
# validate at runtime.
shares: float = 100.0
cash_balance: float = 100_000.00
sectors: list[str] = ["Technology", "Broad Market"]
dividend: float | None = None      # may be absent

print(f"{symbol} - {close:,.2f} x {shares:g} shares")
