"""Shared test setup: isolated SQLite database, seeded demo data, fixture prices.

Tests never call yfinance or the network. Market prices come from
tests/fixtures/prices_sample.csv (AAPL rising, MSFT falling, weekly closes
2020-05-04 through 2020-09-14).
"""

import os
import tempfile
from pathlib import Path

_TEST_DATABASE_DIR = tempfile.mkdtemp(prefix="chronos_test_")
os.environ["CHRONOS_DATABASE_URL"] = (
    f"sqlite:///{_TEST_DATABASE_DIR}/test_chronos.db"
)

import pytest
from fastapi.testclient import TestClient

from chronos.app_startup.seed_demo_users_accounts_and_assets import (
    seed_demo_users_accounts_and_assets,
)
from chronos.market_data_loading_and_price_queries import (
    load_market_prices_into_database,
)
from chronos.market_data_loading_and_price_queries import load_market_prices_from_csv
from chronos.shared_database.database_connection import (
    SessionLocal,
    engine,
    get_database_session,
)
from chronos.shared_database.database_tables import Account, Base, User

FIXTURE_PRICES_CSV = Path(__file__).parent / "fixtures" / "prices_sample.csv"

ALICE_EMAIL = "alice@example.com"
BOB_EMAIL = "bob@example.com"
ADVISOR_EMAIL = "advisor@example.com"


@pytest.fixture()
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    seed_demo_users_accounts_and_assets(session)
    prices = load_market_prices_from_csv(FIXTURE_PRICES_CSV)
    load_market_prices_into_database(session, prices)
    session.commit()
    yield session
    session.rollback()
    session.close()


@pytest.fixture()
def client(db):
    from chronos.main import app

    def _shared_test_session():
        try:
            yield db
            db.flush()
        except Exception:
            db.rollback()
            raise

    app.dependency_overrides[get_database_session] = _shared_test_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def alice(db) -> User:
    return db.query(User).filter(User.email == ALICE_EMAIL).one()


@pytest.fixture()
def advisor(db) -> User:
    return db.query(User).filter(User.email == ADVISOR_EMAIL).one()


@pytest.fixture()
def alice_account(db, alice) -> Account:
    return db.query(Account).filter(Account.user_id == alice.id).one()
