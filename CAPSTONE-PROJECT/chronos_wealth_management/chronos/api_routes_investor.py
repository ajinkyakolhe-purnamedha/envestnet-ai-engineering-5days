"""Investor-facing account, portfolio, trade, and market-data routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from chronos.application_errors_and_permissions import (
    require_investor_user,
    translate_domain_errors,
)
from chronos.demo_users_and_startup_data import get_demo_user_by_id
from chronos.investor_accounts_portfolios_and_history import (
    build_account_value_history,
    build_current_portfolio_snapshot,
    build_investor_account_response,
    get_account_for_investor_user,
    get_symbol_price_history,
)
from chronos.investor_trade_execution_and_preview import (
    execute_investor_trade,
    list_trades_for_investor_account,
    preview_investor_trade,
)
from chronos.market_data_loading_and_price_queries import (
    get_supported_assets,
    require_supported_asset,
)
from chronos.api_schemas_investor import (
    AccountResponse,
    AccountValueHistoryPointResponse,
    AssetResponse,
    MarketPriceHistoryPointResponse,
    PortfolioResponse,
    TradePreviewResponse,
    TradeRequest,
    TradeResponse,
)
from chronos.application_database import get_database_session

router = APIRouter()


@router.get("/account", response_model=AccountResponse)
def read_investor_account(
    user_id: int, db: Session = Depends(get_database_session)
):
    with translate_domain_errors():
        require_investor_user(get_demo_user_by_id(db, user_id))
        account = get_account_for_investor_user(db, user_id)
        return build_investor_account_response(account)


@router.get("/portfolio", response_model=PortfolioResponse)
def read_investor_portfolio(
    user_id: int, db: Session = Depends(get_database_session)
):
    with translate_domain_errors():
        require_investor_user(get_demo_user_by_id(db, user_id))
        account = get_account_for_investor_user(db, user_id)
        return build_current_portfolio_snapshot(db, account)


@router.get(
    "/portfolio/account-value-history",
    response_model=list[AccountValueHistoryPointResponse],
)
def read_account_value_history(
    user_id: int, db: Session = Depends(get_database_session)
):
    with translate_domain_errors():
        require_investor_user(get_demo_user_by_id(db, user_id))
        account = get_account_for_investor_user(db, user_id)
        return build_account_value_history(db, account)


@router.get("/trades", response_model=list[TradeResponse])
def read_investor_trades(
    user_id: int, db: Session = Depends(get_database_session)
):
    with translate_domain_errors():
        require_investor_user(get_demo_user_by_id(db, user_id))
        account = get_account_for_investor_user(db, user_id)
        return list_trades_for_investor_account(db, account.id)


@router.post("/trades/preview", response_model=TradePreviewResponse)
def preview_trade(
    request: TradeRequest, db: Session = Depends(get_database_session)
):
    with translate_domain_errors():
        require_investor_user(get_demo_user_by_id(db, request.user_id))
        account = get_account_for_investor_user(db, request.user_id)
        return preview_investor_trade(db, account, request)


@router.post("/trades", response_model=TradeResponse)
def execute_trade(
    request: TradeRequest, db: Session = Depends(get_database_session)
):
    with translate_domain_errors():
        require_investor_user(get_demo_user_by_id(db, request.user_id))
        account = get_account_for_investor_user(db, request.user_id)
        return execute_investor_trade(db, account, request)


@router.get("/assets", response_model=list[AssetResponse])
def read_supported_assets(db: Session = Depends(get_database_session)):
    return get_supported_assets(db)


@router.get(
    "/market/{symbol}/history",
    response_model=list[MarketPriceHistoryPointResponse],
)
def read_symbol_price_history(
    symbol: str,
    user_id: int,
    trading_days: int = 60,
    db: Session = Depends(get_database_session),
):
    with translate_domain_errors():
        asset = require_supported_asset(db, symbol)
        account = get_account_for_investor_user(db, user_id)
        prices = get_symbol_price_history(
            db, asset.symbol, account.simulated_date, trading_days
        )
    return [
        MarketPriceHistoryPointResponse(
            symbol=price.symbol, date=price.date, close=price.close
        )
        for price in prices
    ]
