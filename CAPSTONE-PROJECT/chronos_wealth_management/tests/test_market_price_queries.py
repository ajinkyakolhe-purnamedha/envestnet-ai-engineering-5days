"""Point-in-time price rule: never look past the simulated date."""

from datetime import date

import pytest

from chronos.market_price_queries.find_price_for_simulated_date import (
    get_latest_price_on_or_before_date,
)
from chronos.market_price_queries.get_symbol_price_history import (
    get_symbol_price_history_until_date,
)
from chronos.shared_database.domain_errors import PriceUnavailableError


def test_price_lookup_uses_latest_on_or_before_date(db):
    price = get_latest_price_on_or_before_date(db, "AAPL", date(2020, 6, 3))
    assert price.date == date(2020, 6, 1)
    assert price.close == 108.0


def test_price_lookup_on_exact_date(db):
    price = get_latest_price_on_or_before_date(db, "AAPL", date(2020, 6, 1))
    assert price.date == date(2020, 6, 1)


def test_price_lookup_before_first_price_fails(db):
    with pytest.raises(PriceUnavailableError):
        get_latest_price_on_or_before_date(db, "AAPL", date(2020, 1, 1))


def test_symbol_history_returns_no_future_prices(db):
    end_date = date(2020, 6, 1)
    history = get_symbol_price_history_until_date(db, "AAPL", end_date)
    assert history
    assert all(price.date <= end_date for price in history)
    assert [price.date for price in history] == sorted(
        price.date for price in history
    )


def test_symbol_history_respects_trading_days_limit(db):
    history = get_symbol_price_history_until_date(
        db, "AAPL", date(2020, 9, 14), trading_days=5
    )
    assert len(history) == 5
    assert history[-1].date == date(2020, 9, 14)

def test_trading_days_beyond_available_returns_everything(db):
    history = get_symbol_price_history_until_date(
        db, "AAPL", date(2020, 9, 14), trading_days=500
    )
    assert len(history) == 20


def test_lowercase_symbol_is_accepted(db):
    from chronos.market_price_queries.find_price_for_simulated_date import (
        require_supported_asset,
    )

    assert require_supported_asset(db, "aapl").symbol == "AAPL"


def test_unknown_symbol_is_rejected(db):
    from chronos.market_price_queries.find_price_for_simulated_date import (
        require_supported_asset,
    )
    from chronos.shared_database.domain_errors import RecordNotFoundError

    with pytest.raises(RecordNotFoundError):
        require_supported_asset(db, "ZZZZ")
