"""Advisor client list with portfolio summaries — read only."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.demo_users.demo_user_login import get_demo_user_by_id
from chronos.demo_users.user_role_permissions import (
    INVESTOR_ROLE,
    require_advisor_user,
)
from chronos.investor_accounts.get_investor_account import (
    get_account_for_investor_user,
)
from chronos.portfolio_performance.calculate_current_portfolio_value import (
    build_current_portfolio_snapshot,
)
from chronos.shared_database.api_schemas import AdvisorClientSummaryResponse
from chronos.shared_database.database_tables import User


def list_clients_for_advisor(
    db: Session, advisor_user_id: int
) -> list[AdvisorClientSummaryResponse]:
    advisor = get_demo_user_by_id(db, advisor_user_id)
    require_advisor_user(advisor)

    clients = db.scalars(
        select(User).where(User.role == INVESTOR_ROLE).order_by(User.id)
    )
    summaries: list[AdvisorClientSummaryResponse] = []
    for client in clients:
        account = get_account_for_investor_user(db, client.id)
        portfolio = build_current_portfolio_snapshot(db, account)
        summaries.append(
            AdvisorClientSummaryResponse(
                client_user_id=client.id,
                client_name=client.name,
                client_email=client.email,
                account_id=account.id,
                simulated_date=account.simulated_date,
                total_value=portfolio.total_value,
                total_return_percentage=portfolio.total_return_percentage,
                number_of_holdings=len(portfolio.holdings),
            )
        )
    return summaries
