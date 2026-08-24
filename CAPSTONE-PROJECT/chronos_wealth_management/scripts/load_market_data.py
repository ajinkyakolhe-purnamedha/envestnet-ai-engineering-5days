"""One-time setup: yfinance -> data/market/prices.csv -> SQLite prices table.

Run from the project root:

    uv run python -m scripts.load_market_data
"""

from chronos.market_data_loading_and_price_queries import (
    download_prices_from_yfinance,
    normalize_yfinance_prices,
)
from chronos.market_data_loading_and_price_queries import (
    load_market_prices_into_database,
)
from chronos.market_data_loading_and_price_queries import save_market_prices_to_csv
from chronos.shared_database.database_connection import (
    MARKET_PRICES_CSV_PATH,
    SessionLocal,
    create_database_tables,
)

SYMBOLS = ["AAPL", "MSFT", "SPY", "GLD", "JPM"]
START_DATE = "2020-01-01"
END_DATE = "2021-12-31"


def main() -> None:
    print(f"Downloading {SYMBOLS} from yfinance ({START_DATE} to {END_DATE})...")
    raw_prices = download_prices_from_yfinance(SYMBOLS, START_DATE, END_DATE)
    prices = normalize_yfinance_prices(raw_prices, SYMBOLS)
    print(f"Normalized {len(prices)} price rows.")

    save_market_prices_to_csv(prices, MARKET_PRICES_CSV_PATH)
    print(f"Saved CSV to {MARKET_PRICES_CSV_PATH}")

    create_database_tables()
    session = SessionLocal()
    try:
        rows_written = load_market_prices_into_database(session, prices)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    print(f"Loaded {rows_written} price rows into SQLite.")


if __name__ == "__main__":
    main()
