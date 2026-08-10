"""Trade preview, execution, and history routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from chronos.api_routes.http_error_translation import translate_domain_errors
from chronos.demo_users.demo_user_login import get_demo_user_by_id
from chronos.demo_users.user_role_permissions import require_investor_user
from chronos.investor_accounts.get_investor_account import (
    get_account_for_investor_user,
)
from chronos.investor_trading.execute_investor_trade import execute_investor_trade
from chronos.investor_trading.list_investor_trades import (
    list_trades_for_investor_account,
)
from chronos.investor_trading.preview_investor_trade import preview_investor_trade
from chronos.shared_database.api_schemas import (
    TradePreviewResponse,
    TradeRequest,
    TradeResponse,
)
from chronos.shared_database.database_connection import get_database_session

router = APIRouter()


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
