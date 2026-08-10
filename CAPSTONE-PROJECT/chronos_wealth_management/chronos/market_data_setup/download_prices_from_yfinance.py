"""Download and normalize historical prices from yfinance.

Only `scripts/load_market_data.py` calls these functions; the running app and
the tests never touch yfinance or the network.
"""

import pandas as pd

CSV_COLUMNS = [
    "symbol",
    "date",
    "open",
    "high",
    "low",
    "close",
    "adjusted_close",
    "volume",
    "source",
]


def download_prices_from_yfinance(
    symbols: list[str], start: str, end: str
) -> pd.DataFrame:
    import yfinance as yf

    upper_symbols = [symbol.upper() for symbol in symbols]
    raw_prices = yf.download(
        upper_symbols,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=False,
        group_by="ticker",
        progress=False,
    )
    if raw_prices is None or raw_prices.empty:
        raise RuntimeError(
            f"yfinance returned no data for {upper_symbols} between {start} and {end}"
        )
    return raw_prices


def normalize_yfinance_prices(
    raw_prices: pd.DataFrame, symbols: list[str] | None = None
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []

    if isinstance(raw_prices.columns, pd.MultiIndex):
        downloaded_symbols = list(raw_prices.columns.get_level_values(0).unique())
        for symbol in downloaded_symbols:
            frames.append(_normalize_single_symbol(raw_prices[symbol], symbol))
    else:
        symbol = (symbols or ["UNKNOWN"])[0].upper()
        frames.append(_normalize_single_symbol(raw_prices, symbol))

    normalized = pd.concat(frames, ignore_index=True)
    normalized = normalized.dropna(subset=["close"])
    normalized = normalized.sort_values(["symbol", "date"]).reset_index(drop=True)
    return normalized[CSV_COLUMNS]


def _normalize_single_symbol(symbol_prices: pd.DataFrame, symbol: str) -> pd.DataFrame:
    frame = symbol_prices.reset_index()
    frame.columns = [str(column) for column in frame.columns]
    adjusted_close = (
        frame["Adj Close"] if "Adj Close" in frame.columns else frame["Close"]
    )
    return pd.DataFrame(
        {
            "symbol": symbol.upper(),
            "date": pd.to_datetime(frame["Date"]).dt.date,
            "open": frame.get("Open"),
            "high": frame.get("High"),
            "low": frame.get("Low"),
            "close": frame["Close"],
            "adjusted_close": adjusted_close,
            "volume": frame.get("Volume"),
            "source": "YFINANCE",
        }
    )
