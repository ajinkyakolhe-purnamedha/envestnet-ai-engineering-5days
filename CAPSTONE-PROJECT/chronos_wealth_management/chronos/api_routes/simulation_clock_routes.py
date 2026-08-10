"""Simulated time advance route with before/after portfolio snapshots."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from chronos.api_routes.http_error_translation import translate_domain_errors
from chronos.demo_users.demo_user_login import get_demo_user_by_id
from chronos.demo_users.user_role_permissions import require_investor_user
from chronos.investor_accounts.get_investor_account import (
    build_investor_account_response,
    get_account_for_investor_user,
)
from chronos.portfolio_performance.calculate_current_portfolio_value import (
    build_current_portfolio_snapshot,
)
from chronos.shared_database.api_schemas import (
    AdvanceSimulationRequest,
    SimulationAdvanceResponse,
)
from chronos.shared_database.database_connection import get_database_session
from chronos.simulation_clock.advance_simulated_investment_date import (
    advance_simulated_investment_date,
)

router = APIRouter()


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
