"""The M7 advisor tools, shared by every framework port.

Same three facts as the M7 deck: price, allocation,
guideline. The framework changes; the tools do not.

Also loads GEMINI_API_KEY from CODE-ALONGS/.env so the
three cloud-backed ports find it on import.
"""

from dotenv import load_dotenv

# override=True: the .env key beats any stale shell export
load_dotenv(override=True)


# #region tools
def get_current_price(symbol: str) -> dict:
    """Latest close for one symbol on the simulated date."""
    prices = {"AAPL": 80.46, "MSFT": 182.83, "GLD": 163.66}
    if symbol not in prices:
        raise ValueError(f"Unknown symbol {symbol}")
    return {"symbol": symbol, "close": prices[symbol]}


def get_portfolio_allocation(client_id: int) -> dict:
    """Current allocation percentages for one client."""
    return {"client_id": client_id,
            "AAPL": 32.0, "MSFT": 24.0, "cash": 18.0}


def check_guidelines(symbol: str,
                     proposed_allocation_pct: float) -> dict:
    """Is the proposed allocation within the 35% limit?"""
    return {"symbol": symbol, "limit_pct": 35.0,
            "allowed": proposed_allocation_pct <= 35.0}
# #endregion tools


QUESTION = ("Can Alice (client 1) raise AAPL to 36% of her "
            "portfolio? Check the current price, her current "
            "allocation, and the guideline before answering.")


if __name__ == "__main__":
    print(get_current_price("AAPL"))
    print(get_portfolio_allocation(1))
    print(check_guidelines("AAPL", 36.0))

# Three deterministic functions. In M7 you wrote the loop
# that decides when to call them. In M8, four different
# frameworks make that decision for you -- around these
# exact same tools.
