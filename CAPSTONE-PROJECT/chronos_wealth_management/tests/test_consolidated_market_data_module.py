import chronos.market_data_loading_and_price_queries as market_data

from chronos.market_data_loading_and_price_queries import (
    ensure_market_prices_loaded,
    get_latest_price_on_or_before_date,
    load_market_prices_into_database,
    load_market_prices_from_csv,
)


def test_market_data_module_exports_canonical_functions_only():
    assert ensure_market_prices_loaded.__name__ == "ensure_market_prices_loaded"
    assert load_market_prices_into_database.__name__ == "load_market_prices_into_database"
    assert not hasattr(market_data, "find_price_for_simulated_date")
    assert not hasattr(market_data, "load_prices_into_database")


def test_market_data_owner_exports_its_behavior():
    assert all(function.__module__ == "chronos.market_data_loading_and_price_queries" for function in (
        ensure_market_prices_loaded,
        get_latest_price_on_or_before_date,
        load_market_prices_from_csv,
        load_market_prices_into_database,
    ))
