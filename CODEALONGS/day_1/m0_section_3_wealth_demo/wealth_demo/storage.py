"""SQLite persistence for the synthetic wealth demo."""

import logging
import sqlite3

from wealth_demo.models import Holding


logger = logging.getLogger(__name__)


def create_database(connection: sqlite3.Connection) -> None:
    """Create the two small tables used by the demo."""
    connection.execute(
        "CREATE TABLE IF NOT EXISTS holdings (symbol TEXT, shares INTEGER, purchase_price REAL)"
    )
    connection.execute(
        "CREATE TABLE IF NOT EXISTS prices (symbol TEXT, date TEXT, close REAL)"
    )
    connection.commit()


def seed_prices(connection: sqlite3.Connection) -> None:
    """Insert a tiny, synthetic AAPL price history."""
    connection.executemany(
        "INSERT INTO prices VALUES (?, ?, ?)",
        [
            ("AAPL", "2020-05-29", 79.49),
            ("AAPL", "2020-06-01", 80.46),
            ("AAPL", "2020-06-02", 80.83),
        ],
    )
    connection.commit()


def save_holding(connection: sqlite3.Connection, holding: Holding) -> None:
    """Store one holding in SQLite."""
    connection.execute(
        "INSERT INTO holdings VALUES (?, ?, ?)",
        (holding.symbol, holding.shares, holding.purchase_price),
    )
    connection.commit()


def load_holdings(connection: sqlite3.Connection) -> list[Holding]:
    """Load all stored holdings."""
    logger.info("Loading holdings from database")
    rows = connection.execute("SELECT symbol, shares, purchase_price FROM holdings")
    return [Holding(*row) for row in rows]


def get_price_as_of(connection: sqlite3.Connection, symbol: str, as_of: str) -> float:
    """Return the last available close on or before an ISO date."""
    row = connection.execute(
        "SELECT date, close FROM prices WHERE symbol = ? AND date <= ? "
        "ORDER BY date DESC LIMIT 1",
        (symbol, as_of),
    ).fetchone()
    if row is None:
        raise ValueError(f"No {symbol} price on or before {as_of}.")
    selected_date, close = row
    logger.info("Selected %s price dated %s", symbol, selected_date)
    return close
