"""Advisor workspace read-only client routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from chronos.advisor_client_lists import list_clients_for_advisor
from chronos.application_errors_and_permissions import (
    require_advisor_user,
    require_investor_user,
    translate_domain_errors,
)
from chronos.demo_users_and_startup_data import get_demo_user_by_id
from chronos.investor_accounts_portfolios_and_history import (
    build_current_portfolio_snapshot,
    get_account_for_investor_user,
)
from chronos.api_schemas_advisor import AdvisorClientSummaryResponse
from chronos.api_schemas_investor import PortfolioResponse
from chronos.application_database import get_database_session

router = APIRouter()


@router.get("/advisor/clients", response_model=list[AdvisorClientSummaryResponse])
def read_advisor_clients(
    advisor_user_id: int, db: Session = Depends(get_database_session)
):
    with translate_domain_errors():
        return list_clients_for_advisor(db, advisor_user_id)


@router.get(
    "/advisor/clients/{client_user_id}/portfolio", response_model=PortfolioResponse
)
def read_advisor_client_portfolio(
    client_user_id: int,
    advisor_user_id: int,
    db: Session = Depends(get_database_session),
):
    with translate_domain_errors():
        require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
        require_investor_user(get_demo_user_by_id(db, client_user_id))
        account = get_account_for_investor_user(db, client_user_id)
        return build_current_portfolio_snapshot(db, account)
