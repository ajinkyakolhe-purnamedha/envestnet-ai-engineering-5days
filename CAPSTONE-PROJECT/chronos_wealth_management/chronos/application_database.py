"""Database tables and session helpers for Chronos Wealth."""

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chronos.shared_database.database_tables import (
    Account,
    AdvisorNoteDraft,
    AdvisorReport,
    Asset,
    Base,
    Holding,
    Price,
    Trade,
    User,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "data" / "chronos.db"
MARKET_PRICES_CSV_PATH = PROJECT_ROOT / "data" / "market" / "prices.csv"


def _build_database_url() -> str:
    configured_url = os.environ.get("CHRONOS_DATABASE_URL")
    if configured_url:
        return configured_url
    DEFAULT_DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{DEFAULT_DATABASE_PATH}"


DATABASE_URL = _build_database_url()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def create_database_tables() -> None:
    Base.metadata.create_all(bind=engine)


def get_database_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
