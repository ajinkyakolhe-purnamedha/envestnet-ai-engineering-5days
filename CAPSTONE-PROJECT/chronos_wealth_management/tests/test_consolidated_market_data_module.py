from chronos.market_data_loading_and_price_queries import (
    ensure_market_prices_loaded,
    find_price_for_simulated_date,
    get_latest_price_on_or_before_date,
    load_market_prices_from_csv,
    load_prices_into_database,
    load_market_prices_into_database,
)


def test_market_data_module_exports_expected_functions():
    assert ensure_market_prices_loaded.__name__ == "ensure_market_prices_loaded"
    assert find_price_for_simulated_date.__name__ == "find_price_for_simulated_date"
    assert load_prices_into_database.__name__ == "load_prices_into_database"


def test_market_data_owner_exports_its_behavior():
    assert all(function.__module__ == "chronos.market_data_loading_and_price_queries" for function in (
        ensure_market_prices_loaded,
        find_price_for_simulated_date,
        get_latest_price_on_or_before_date,
        load_market_prices_from_csv,
        load_prices_into_database,
        load_market_prices_into_database,
    ))
