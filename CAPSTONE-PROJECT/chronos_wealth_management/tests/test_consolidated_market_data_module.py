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


def test_legacy_market_setup_modules_delegate_to_consolidated_owner():
    from chronos.market_data_setup.load_prices_into_database import (
        ensure_market_prices_loaded as legacy_ensure_market_prices_loaded,
    )
    from chronos.market_data_setup.load_prices_into_database import (
        load_market_prices_into_database as legacy_load_market_prices_into_database,
    )
    from chronos.market_data_setup.save_prices_to_csv import (
        load_market_prices_from_csv as legacy_load_market_prices_from_csv,
    )

    assert legacy_ensure_market_prices_loaded is ensure_market_prices_loaded
    assert legacy_load_market_prices_into_database is load_market_prices_into_database
    assert legacy_load_market_prices_from_csv is load_market_prices_from_csv


def test_legacy_point_in_time_query_delegates_to_consolidated_owner():
    from chronos.market_price_queries.find_price_for_simulated_date import (
        get_latest_price_on_or_before_date as legacy_get_latest_price,
    )

    assert legacy_get_latest_price is get_latest_price_on_or_before_date
