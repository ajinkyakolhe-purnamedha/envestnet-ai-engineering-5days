"""Chronos Wealth FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from chronos.api_routes import (
    advisor_workspace_routes,
    demo_user_routes,
    investor_account_routes,
    investor_trade_routes,
    market_price_routes,
    simulation_clock_routes,
)
from chronos.app_startup.seed_demo_users_accounts_and_assets import (
    seed_demo_users_accounts_and_assets,
)
from chronos.market_data_loading_and_price_queries import (
    ensure_market_prices_loaded,
)
from chronos.shared_database.database_connection import (
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

app.include_router(demo_user_routes.router)
app.include_router(market_price_routes.router)
app.include_router(investor_account_routes.router)
app.include_router(investor_trade_routes.router)
app.include_router(simulation_clock_routes.router)
app.include_router(advisor_workspace_routes.router)
