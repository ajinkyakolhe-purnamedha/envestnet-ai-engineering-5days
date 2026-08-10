"""Fixture CSV loads into SQLite; reloads never duplicate (symbol, date)."""

import pytest
from sqlalchemy import func, select

import chronos.market_data_setup.load_prices_into_database as price_loading
from chronos.market_data_setup.load_prices_into_database import (
    ensure_market_prices_loaded,
    load_market_prices_into_database,
)
from chronos.shared_database.domain_errors import MarketDataSetupError
from chronos.market_data_setup.save_prices_to_csv import load_market_prices_from_csv
from chronos.shared_database.database_tables import Price
from tests.conftest import FIXTURE_PRICES_CSV


def test_fixture_csv_loads_into_sqlite(db):
    row_count = db.scalar(select(func.count(Price.id)))
    assert row_count == 40
    symbols = set(db.scalars(select(Price.symbol).distinct()))
    assert symbols == {"AAPL", "MSFT"}


def test_duplicate_load_does_not_duplicate_symbol_date(db):
    prices = load_market_prices_from_csv(FIXTURE_PRICES_CSV)
    load_market_prices_into_database(db, prices)
    db.commit()

    total_rows = db.scalar(select(func.count(Price.id)))
    distinct_pairs = db.scalar(
        select(func.count()).select_from(
            select(Price.symbol, Price.date).distinct().subquery()
        )
    )
    assert total_rows == 40
    assert distinct_pairs == 40

def test_reload_updates_changed_close_instead_of_duplicating(db):
    prices = load_market_prices_from_csv(FIXTURE_PRICES_CSV)
    prices.loc[
        (prices["symbol"] == "AAPL") & (prices["date"] == prices["date"].min()),
        "close",
    ] = 999.0
    load_market_prices_into_database(db, prices)
    db.commit()

    from chronos.shared_database.database_tables import Price

    updated = db.scalar(
        select(Price.close)
        .where(Price.symbol == "AAPL")
        .order_by(Price.date)
        .limit(1)
    )
    assert updated == 999.0
    assert db.scalar(select(func.count(Price.id))) == 40


def test_csv_with_missing_columns_is_rejected(tmp_path):
    from chronos.market_data_setup.save_prices_to_csv import (
        load_market_prices_from_csv as load_csv,
    )

    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("symbol,date,close\nAAPL,2020-06-01,108\n")
    with pytest.raises(ValueError, match="missing required columns"):
        load_csv(bad_csv)


def test_ensure_prices_errors_when_database_and_csv_are_both_empty(
    db, tmp_path, monkeypatch
):
    from chronos.shared_database.database_tables import Price

    db.query(Price).delete()
    db.flush()
    monkeypatch.setattr(
        price_loading, "MARKET_PRICES_CSV_PATH", tmp_path / "missing.csv"
    )
    with pytest.raises(MarketDataSetupError, match="load_market_data"):
        ensure_market_prices_loaded(db)


def test_ensure_prices_is_a_no_op_when_prices_exist(db):
    ensure_market_prices_loaded(db)  # must not raise or need the CSV

    from chronos.shared_database.database_tables import Price

    assert db.scalar(select(func.count(Price.id))) == 40
