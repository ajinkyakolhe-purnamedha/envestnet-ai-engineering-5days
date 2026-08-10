"""Load CSV prices into the SQLite prices table."""

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.shared_database.database_connection import MARKET_PRICES_CSV_PATH
from chronos.shared_database.database_tables import Price
from chronos.shared_database.domain_errors import MarketDataSetupError
from chronos.market_data_setup.save_prices_to_csv import load_market_prices_from_csv


def load_market_prices_into_database(db: Session, prices: pd.DataFrame) -> int:
    rows_written = 0
    for row in prices.itertuples(index=False):
        existing_price = db.scalar(
            select(Price).where(Price.symbol == row.symbol, Price.date == row.date)
        )
        if existing_price is None:
            db.add(
                Price(
                    symbol=row.symbol,
                    date=row.date,
                    open=_optional_float(row.open),
                    high=_optional_float(row.high),
                    low=_optional_float(row.low),
                    close=float(row.close),
                    adjusted_close=_optional_float(row.adjusted_close),
                    volume=_optional_int(row.volume),
                    source=str(row.source),
                )
            )
        else:
            existing_price.open = _optional_float(row.open)
            existing_price.high = _optional_float(row.high)
            existing_price.low = _optional_float(row.low)
            existing_price.close = float(row.close)
            existing_price.adjusted_close = _optional_float(row.adjusted_close)
            existing_price.volume = _optional_int(row.volume)
            existing_price.source = str(row.source)
        rows_written += 1
    db.flush()
    return rows_written


def ensure_market_prices_loaded(db: Session) -> None:
    if db.scalar(select(Price.id).limit(1)) is not None:
        return
    if not MARKET_PRICES_CSV_PATH.exists():
        raise MarketDataSetupError(
            f"No market prices found in the database and {MARKET_PRICES_CSV_PATH} "
            "does not exist. Run: uv run python -m scripts.load_market_data"
        )
    prices = load_market_prices_from_csv(MARKET_PRICES_CSV_PATH)
    load_market_prices_into_database(db, prices)


def _optional_float(value) -> float | None:
    if value is None or pd.isna(value):
        return None
    return float(value)


def _optional_int(value) -> int | None:
    if value is None or pd.isna(value):
        return None
    return int(value)
