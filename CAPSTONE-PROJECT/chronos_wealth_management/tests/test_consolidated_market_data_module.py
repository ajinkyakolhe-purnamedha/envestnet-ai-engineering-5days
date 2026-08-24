from chronos.market_data_loading_and_price_queries import (
    ensure_market_prices_loaded,
    find_price_for_simulated_date,
    load_prices_into_database,
)


def test_market_data_module_exports_expected_functions():
    assert ensure_market_prices_loaded.__name__ == "ensure_market_prices_loaded"
    assert find_price_for_simulated_date.__name__ == "find_price_for_simulated_date"
    assert load_prices_into_database.__name__ == "load_prices_into_database"
