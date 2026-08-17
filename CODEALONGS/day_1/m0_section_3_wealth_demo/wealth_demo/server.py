"""FastAPI routes for the synthetic wealth demo."""

import logging
import sqlite3

from fastapi import FastAPI, HTTPException

from wealth_demo.models import Holding, Portfolio
from wealth_demo.storage import create_database, get_price_as_of, load_holdings, save_holding, seed_prices


logger = logging.getLogger(__name__)
app = FastAPI(title="Wealth Demo")


def portfolio_payload() -> dict:
    """Build the demo portfolio response from synthetic SQLite data."""
    connection = sqlite3.connect(":memory:")
    create_database(connection)
    seed_prices(connection)
    save_holding(connection, Holding("AAPL", 10, 80.50))
    holdings = load_holdings(connection)
    portfolio = Portfolio(cash=1_000.0)
    for holding in holdings:
        portfolio.buy(holding)
    latest_prices = {"AAPL": get_price_as_of(connection, "AAPL", "2020-06-02")}
    return {
        "cash": portfolio.cash,
        "total_value": portfolio.total_value(latest_prices),
        "holdings": [holding.__dict__ for holding in holdings],
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Confirm that the application is running."""
    return {"status": "ok"}


@app.get("/portfolio")
def portfolio() -> dict:
    """Return the synthetic portfolio as JSON."""
    logger.info("Serving portfolio request")
    try:
        return portfolio_payload()
    except sqlite3.Error as error:
        logger.exception("Unexpected database error")
        raise HTTPException(status_code=500, detail="database failure") from error
