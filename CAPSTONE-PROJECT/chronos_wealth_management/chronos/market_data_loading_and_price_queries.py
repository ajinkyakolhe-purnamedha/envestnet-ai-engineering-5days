"""Market-data loading and point-in-time price query entry points."""

from chronos.market_data_setup.load_prices_into_database import (
    ensure_market_prices_loaded,
    load_market_prices_into_database,
)
from chronos.market_price_queries.find_price_for_simulated_date import (
    get_latest_price_on_or_before_date,
)


def find_price_for_simulated_date(db, symbol, simulated_date):
    """Find the latest available price on or before the simulated date."""
    return get_latest_price_on_or_before_date(db, symbol, simulated_date)


def load_prices_into_database(db, prices):
    """Load normalized market prices into the application database."""
    return load_market_prices_into_database(db, prices)
