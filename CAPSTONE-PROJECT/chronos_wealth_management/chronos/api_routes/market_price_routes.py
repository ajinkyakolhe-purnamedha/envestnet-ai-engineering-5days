"""Asset listing and point-in-time symbol price history routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from chronos.api_routes.http_error_translation import translate_domain_errors
from chronos.investor_accounts_portfolios_and_history import get_account_for_investor_user, get_symbol_price_history
from chronos.market_data_loading_and_price_queries import (
    get_supported_assets,
    require_supported_asset,
)
from chronos.shared_database.api_schemas import (
    AssetResponse,
    MarketPriceHistoryPointResponse,
)
from chronos.shared_database.database_connection import get_database_session

router = APIRouter()


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
