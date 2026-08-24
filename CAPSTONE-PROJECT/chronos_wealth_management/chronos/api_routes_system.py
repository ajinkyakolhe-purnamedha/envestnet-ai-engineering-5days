"""System, authentication, demo reset, and simulated-time routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from chronos.api_routes.http_error_translation import translate_domain_errors
from chronos.app_startup.seed_demo_users_accounts_and_assets import (
    reset_demo_investor_accounts,
)
from chronos.demo_users.demo_user_login import (
    get_demo_user_by_id,
    list_demo_users,
    login_demo_user_by_email,
)
from chronos.demo_users.user_role_permissions import require_investor_user
from chronos.investor_accounts_portfolios_and_history import (
    advance_simulated_investment_date,
    build_current_portfolio_snapshot,
    build_investor_account_response,
    get_account_for_investor_user,
)
from chronos.shared_database.api_schemas import (
    AdvanceSimulationRequest,
    DemoResetResponse,
    LoginRequest,
    SimulationAdvanceResponse,
    UserResponse,
)
from chronos.shared_database.database_connection import get_database_session

router = APIRouter()


@router.get("/health")
def read_health() -> dict:
    return {"status": "ok"}


@router.get("/auth/demo-users", response_model=list[UserResponse])
def read_demo_users(db: Session = Depends(get_database_session)):
    return list_demo_users(db)


@router.post("/auth/login", response_model=UserResponse)
def login_demo_user(
    request: LoginRequest, db: Session = Depends(get_database_session)
):
    with translate_domain_errors():
        return login_demo_user_by_email(db, request.email)


@router.post("/demo/reset", response_model=DemoResetResponse)
def reset_demo_data(db: Session = Depends(get_database_session)):
    return DemoResetResponse(accounts_reset=reset_demo_investor_accounts(db))


@router.post("/simulation/advance", response_model=SimulationAdvanceResponse)
def advance_simulation(
    request: AdvanceSimulationRequest, db: Session = Depends(get_database_session)
):
    with translate_domain_errors():
        require_investor_user(get_demo_user_by_id(db, request.user_id))
        account = get_account_for_investor_user(db, request.user_id)
        previous_portfolio = build_current_portfolio_snapshot(db, account)
        account = advance_simulated_investment_date(db, account, request.step)
        portfolio = build_current_portfolio_snapshot(db, account)
    return SimulationAdvanceResponse(
        account=build_investor_account_response(account),
        previous_portfolio=previous_portfolio,
        portfolio=portfolio,
    )
