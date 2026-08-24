"""Market-data setup, loading, and point-in-time price query behavior."""

from datetime import date
from pathlib import Path

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.application_database import MARKET_PRICES_CSV_PATH, Asset, Price
from chronos.application_errors_and_permissions import (
    MarketDataSetupError,
    PriceUnavailableError,
    RecordNotFoundError,
)

CSV_COLUMNS = [
    "symbol", "date", "open", "high", "low", "close", "adjusted_close", "volume", "source",
]


def download_prices_from_yfinance(symbols: list[str], start: str, end: str) -> pd.DataFrame:
    """Download daily historical prices for the requested symbols."""
    import yfinance as yf

    upper_symbols = [symbol.upper() for symbol in symbols]
    raw_prices = yf.download(
        upper_symbols, start=start, end=end, interval="1d", auto_adjust=False,
        group_by="ticker", progress=False,
    )
    if raw_prices is None or raw_prices.empty:
        raise RuntimeError(
            f"yfinance returned no data for {upper_symbols} between {start} and {end}"
        )
    return raw_prices


def normalize_yfinance_prices(raw_prices: pd.DataFrame, symbols: list[str] | None = None) -> pd.DataFrame:
    """Convert yfinance output into Chronos's portable CSV schema."""
    if isinstance(raw_prices.columns, pd.MultiIndex):
        frames = [
            _normalize_single_symbol(raw_prices[symbol], symbol)
            for symbol in raw_prices.columns.get_level_values(0).unique()
        ]
    else:
        frames = [_normalize_single_symbol(raw_prices, (symbols or ["UNKNOWN"])[0])]
    normalized = pd.concat(frames, ignore_index=True).dropna(subset=["close"])
    return normalized.sort_values(["symbol", "date"]).reset_index(drop=True)[CSV_COLUMNS]


def save_market_prices_to_csv(prices: pd.DataFrame, output_path: Path) -> Path:
    """Save normalized market prices to a portable CSV file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prices.to_csv(output_path, index=False)
    return output_path


def load_market_prices_from_csv(input_path: Path) -> pd.DataFrame:
    """Load and validate normalized market prices from CSV."""
    input_path = Path(input_path)
    prices = pd.read_csv(input_path)
    missing_columns = [column for column in CSV_COLUMNS if column not in prices.columns]
    if missing_columns:
        raise ValueError(f"{input_path} is missing required columns: {missing_columns}")
    prices["date"] = pd.to_datetime(prices["date"]).dt.date
    return prices


def load_market_prices_into_database(db: Session, prices: pd.DataFrame) -> int:
    """Insert or update normalized prices without duplicating symbol/date rows."""
    rows_written = 0
    for row in prices.itertuples(index=False):
        existing_price = db.scalar(
            select(Price).where(Price.symbol == row.symbol, Price.date == row.date)
        )
        if existing_price is None:
            db.add(Price(
                symbol=row.symbol, date=row.date, open=_optional_float(row.open),
                high=_optional_float(row.high), low=_optional_float(row.low),
                close=float(row.close), adjusted_close=_optional_float(row.adjusted_close),
                volume=_optional_int(row.volume), source=str(row.source),
            ))
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
    """Load the fixture CSV only when the application database has no prices."""
    if db.scalar(select(Price.id).limit(1)) is not None:
        return
    if not MARKET_PRICES_CSV_PATH.exists():
        raise MarketDataSetupError(
            f"No market prices found in the database and {MARKET_PRICES_CSV_PATH} "
            "does not exist. Run: uv run python -m scripts.load_market_data"
        )
    load_market_prices_into_database(db, load_market_prices_from_csv(MARKET_PRICES_CSV_PATH))


def get_latest_price_on_or_before_date(db: Session, symbol: str, simulated_date: date) -> Price:
    """Return the latest available price, never after the simulated date."""
    price = db.scalar(
        select(Price).where(Price.symbol == symbol, Price.date <= simulated_date)
        .order_by(Price.date.desc()).limit(1)
    )
    if price is None:
        raise PriceUnavailableError(f"No price for {symbol} on or before {simulated_date}")
    return price


def find_price_for_simulated_date(db: Session, symbol: str, simulated_date: date) -> Price:
    """Compatibility-friendly name for the point-in-time price lookup."""
    return get_latest_price_on_or_before_date(db, symbol, simulated_date)


def get_supported_assets(db: Session) -> list[Asset]:
    return list(db.scalars(select(Asset).order_by(Asset.symbol)))


def require_supported_asset(db: Session, symbol: str) -> Asset:
    asset = db.get(Asset, symbol.upper())
    if asset is None:
        raise RecordNotFoundError(f"Unknown symbol {symbol!r}")
    return asset


def load_prices_into_database(db: Session, prices: pd.DataFrame) -> int:
    """Compatibility-friendly name for loading normalized prices."""
    return load_market_prices_into_database(db, prices)


def _normalize_single_symbol(symbol_prices: pd.DataFrame, symbol: str) -> pd.DataFrame:
    frame = symbol_prices.reset_index()
    frame.columns = [str(column) for column in frame.columns]
    adjusted_close = frame["Adj Close"] if "Adj Close" in frame.columns else frame["Close"]
    return pd.DataFrame({
        "symbol": symbol.upper(), "date": pd.to_datetime(frame["Date"]).dt.date,
        "open": frame.get("Open"), "high": frame.get("High"), "low": frame.get("Low"),
        "close": frame["Close"], "adjusted_close": adjusted_close,
        "volume": frame.get("Volume"), "source": "YFINANCE",
    })


def _optional_float(value) -> float | None:
    return None if value is None or pd.isna(value) else float(value)


def _optional_int(value) -> int | None:
    return None if value is None or pd.isna(value) else int(value)
