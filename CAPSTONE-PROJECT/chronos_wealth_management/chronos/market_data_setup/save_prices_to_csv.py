"""Save normalized prices to CSV and read them back."""

from pathlib import Path

import pandas as pd

from chronos.market_data_setup.download_prices_from_yfinance import CSV_COLUMNS


def save_market_prices_to_csv(prices: pd.DataFrame, output_path: Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prices.to_csv(output_path, index=False)
    return output_path


def load_market_prices_from_csv(input_path: Path) -> pd.DataFrame:
    input_path = Path(input_path)
    prices = pd.read_csv(input_path)
    missing_columns = [
        column for column in CSV_COLUMNS if column not in prices.columns
    ]
    if missing_columns:
        raise ValueError(
            f"{input_path} is missing required columns: {missing_columns}"
        )
    prices["date"] = pd.to_datetime(prices["date"]).dt.date
    return prices
