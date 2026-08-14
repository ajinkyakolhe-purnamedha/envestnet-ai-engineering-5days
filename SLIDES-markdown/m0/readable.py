"""Chronos: find the positions that are too big.

Run:
    uv run --project ../CODE-ALONGS \
        python m0/readable.py
"""

holdings = [
    {"symbol": "AAPL", "weight": 0.52},
    {"symbol": "MSFT", "weight": 0.31},
    {"symbol": "GLD", "weight": 0.17},
]

for holding in holdings:
    if holding["weight"] > 0.35:
        print(f"Concentrated: {holding['symbol']}")
