"""GIVEN: gather every fact the assistant may cite — app plumbing.

Sequential on purpose: these lookups share one SQLAlchemy session, and
sessions are not thread-safe. The parallel fan-out pattern (M8.2.4)
applies to independent services with their own connections — not here.
All prices are point-in-time via the portfolio snapshot.
"""

from sqlalchemy.orm import Session

from chronos.advisor_analysis_reports_and_client_lists import (
    analyze_client_portfolio,
    build_advisor_recommendations,
)
from chronos.investor_accounts_portfolios_and_history import (
    get_account_for_investor_user,
)
from chronos.api_schemas_advisor import AdvisorMetricResponse
from chronos.api_schemas_investor import PortfolioResponse
from chronos.investor_accounts_portfolios_and_history import (
    build_current_portfolio_snapshot,
)


def gather_client_facts(
    db: Session, client_user_id: int
) -> tuple[PortfolioResponse, AdvisorMetricResponse, list[str]]:
    account = get_account_for_investor_user(db, client_user_id)
    portfolio = build_current_portfolio_snapshot(db, account)
    metrics = analyze_client_portfolio(portfolio)
    recommendations = build_advisor_recommendations(portfolio)
    return portfolio, metrics, recommendations
