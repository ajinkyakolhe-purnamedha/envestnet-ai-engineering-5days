"""One concept: direct Python tools are trapped inside one application."""


def portfolio_summary(client_id: str) -> dict:
    return {"client": client_id, "cash": 25_000, "holdings": ["SPY", "QQQ", "GLD"]}


def search_policy(query: str) -> dict:
    return {"query": query, "evidence": "No single asset may exceed 35% of the portfolio."}


print("Advisor imports portfolio tool:", portfolio_summary("alice"))
print("Advisor imports policy tool:", search_policy("concentration limit"))
print("Question: how can another application reuse these without importing this file?")
