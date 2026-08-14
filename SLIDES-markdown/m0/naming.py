"""Same behaviour. One of these you can maintain.

Run:
    uv run --project ../CODE-ALONGS \
        python m0/naming.py
"""


# #region before
# proc.py
def proc(d, f=0):
    r = []
    for x in d:
        if x["w"] > 0.35 and (not f or x["s"] == f):
            r.append(x)
    return r
# #endregion before


# #region after
# portfolio_performance/concentration.py
def concentrated_holdings(
    holdings: list[dict],
    sector: str | None = None,
) -> list[dict]:
    """Positions over 35% of the book, in one sector."""
    return [
        holding for holding in holdings
        if holding["weight"] > 0.35
        and (sector is None or holding["sector"] == sector)
    ]
# #endregion after


book = [
    {"symbol": "AAPL", "weight": 0.52,
     "sector": "Technology"},
    {"symbol": "GLD", "weight": 0.17, "sector": "Metals"},
]
print(concentrated_holdings(book))
