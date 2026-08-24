"""Investor account, portfolio, and account value history routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from chronos.api_routes.http_error_translation import translate_domain_errors
from chronos.demo_users.demo_user_login import get_demo_user_by_id
from chronos.demo_users.user_role_permissions import require_investor_user
from chronos.investor_accounts_portfolios_and_history import (
    build_investor_account_response,
    build_current_portfolio_snapshot,
    build_account_value_history,
    get_account_for_investor_user,
)
from chronos.shared_database.api_schemas import (
    AccountResponse,
    AccountValueHistoryPointResponse,
    PortfolioResponse,
)
from chronos.shared_database.database_connection import get_database_session

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
