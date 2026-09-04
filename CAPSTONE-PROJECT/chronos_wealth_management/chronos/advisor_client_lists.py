"""Read-only advisor client summaries."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.api_schemas_advisor import AdvisorClientSummaryResponse
from chronos.application_database import User
from chronos.application_errors_and_permissions import require_advisor_user
from chronos.demo_users_and_startup_data import get_demo_user_by_id
from chronos.investor_accounts_portfolios_and_history import (
    build_current_portfolio_snapshot,
    get_account_for_investor_user,
)


def list_clients_for_advisor(
    db: Session, advisor_user_id: int
) -> list[AdvisorClientSummaryResponse]:
    require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
    clients = db.scalars(
        select(User).where(User.role == "INVESTOR").order_by(User.id)
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
