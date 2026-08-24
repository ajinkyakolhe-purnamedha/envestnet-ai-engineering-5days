"""Chronos Wealth FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from chronos import api_routes_advisor, api_routes_investor, api_routes_system
from chronos.demo_users_and_startup_data import (
    seed_demo_users_accounts_and_assets,
)
from chronos.market_data_loading_and_price_queries import (
    ensure_market_prices_loaded,
)
from chronos.application_database import (
    SessionLocal,
    create_database_tables,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_tables()
    session = SessionLocal()
    try:
        seed_demo_users_accounts_and_assets(session)
        ensure_market_prices_loaded(session)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    yield


app = FastAPI(title="Chronos Wealth", lifespan=lifespan)

app.include_router(api_routes_system.router)
app.include_router(api_routes_investor.router)
app.include_router(api_routes_advisor.router)
