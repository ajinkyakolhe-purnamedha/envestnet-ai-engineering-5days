"""Production owner for deterministic advisor analysis, client lists, and reports."""

import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.demo_users_and_startup_data import get_demo_user_by_id
from chronos.application_errors_and_permissions import (
    INVESTOR_ROLE,
    require_advisor_user,
    require_investor_user,
)
from chronos.investor_accounts_portfolios_and_history import (
    build_current_portfolio_snapshot,
    get_account_for_investor_user,
)
from chronos.api_schemas_advisor import (
    AdvisorClientSummaryResponse,
    AdvisorMetricResponse,
    AdvisorReportResponse,
)
from chronos.api_schemas_investor import PortfolioResponse
from chronos.application_database import AdvisorReport, User
from chronos.application_errors_and_permissions import RecordNotFoundError

CONCENTRATION_THRESHOLD = 0.35
HIGH_CASH_THRESHOLD = 0.40


def analyze_client_portfolio(portfolio: PortfolioResponse) -> AdvisorMetricResponse:
    """Calculate advisor metrics from a supplied snapshot, never from a model."""
    total_value = portfolio.total_value
    cash_ratio = portfolio.cash_balance / total_value if total_value else 0.0
    largest_position_ratio = 0.0
    largest_position_symbol: str | None = None
    best_holding = worst_holding = None
    for holding in portfolio.holdings:
        position_ratio = holding.market_value / total_value if total_value else 0.0
        if position_ratio > largest_position_ratio:
            largest_position_ratio, largest_position_symbol = position_ratio, holding.symbol
        if best_holding is None or holding.unrealized_gain_loss > best_holding.unrealized_gain_loss:
            best_holding = holding
        if worst_holding is None or holding.unrealized_gain_loss < worst_holding.unrealized_gain_loss:
            worst_holding = holding
    return AdvisorMetricResponse(
        total_value=total_value, cash_ratio=cash_ratio,
        largest_position_ratio=largest_position_ratio,
        largest_position_symbol=largest_position_symbol,
        total_return_percentage=portfolio.total_return_percentage,
        number_of_holdings=len(portfolio.holdings),
        best_holding_symbol=best_holding.symbol if best_holding else None,
        best_holding_gain_loss=best_holding.unrealized_gain_loss if best_holding else None,
        worst_holding_symbol=worst_holding.symbol if worst_holding else None,
        worst_holding_gain_loss=worst_holding.unrealized_gain_loss if worst_holding else None,
    )


def build_advisor_recommendations(portfolio: PortfolioResponse) -> list[str]:
    metrics = analyze_client_portfolio(portfolio)
    recommendations: list[str] = []
    if metrics.largest_position_ratio > CONCENTRATION_THRESHOLD:
        recommendations.append(
            f"Concentration risk: {metrics.largest_position_symbol} is "
            f"{metrics.largest_position_ratio:.0%} of the portfolio "
            f"(threshold {CONCENTRATION_THRESHOLD:.0%})."
        )
    if metrics.cash_ratio > HIGH_CASH_THRESHOLD:
        recommendations.append(
            f"High cash allocation: {metrics.cash_ratio:.0%} of the portfolio "
            f"is cash (threshold {HIGH_CASH_THRESHOLD:.0%})."
        )
    if metrics.number_of_holdings == 1:
        recommendations.append("Low diversification: the portfolio has a single holding.")
    if metrics.total_return_percentage < 0:
        recommendations.append(f"Performance review: total return is {metrics.total_return_percentage:.2f}%.")
    if metrics.number_of_holdings == 0:
        recommendations.append("Starting allocation discussion: the portfolio has no holdings yet.")
    return recommendations


def list_clients_for_advisor(db: Session, advisor_user_id: int) -> list[AdvisorClientSummaryResponse]:
    require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
    clients = db.scalars(select(User).where(User.role == INVESTOR_ROLE).order_by(User.id))
    summaries: list[AdvisorClientSummaryResponse] = []
    for client in clients:
        account = get_account_for_investor_user(db, client.id)
        portfolio = build_current_portfolio_snapshot(db, account)
        summaries.append(AdvisorClientSummaryResponse(
            client_user_id=client.id, client_name=client.name, client_email=client.email,
            account_id=account.id, simulated_date=account.simulated_date,
            total_value=portfolio.total_value,
            total_return_percentage=portfolio.total_return_percentage,
            number_of_holdings=len(portfolio.holdings),
        ))
    return summaries


def generate_advisor_review_report(db: Session, advisor_user_id: int, client_user_id: int) -> AdvisorReportResponse:
    advisor = require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
    client = require_investor_user(get_demo_user_by_id(db, client_user_id))
    account = get_account_for_investor_user(db, client.id)
    portfolio = build_current_portfolio_snapshot(db, account)
    metrics = analyze_client_portfolio(portfolio)
    recommendations = build_advisor_recommendations(portfolio)
    summary = (
        f"As of {account.simulated_date}, {client.name}'s portfolio is worth "
        f"${metrics.total_value:,.2f} ({metrics.total_return_percentage:+.2f}% total return) "
        f"across {metrics.number_of_holdings} holdings, with {len(recommendations)} advisory flags."
    )
    report = AdvisorReport(
        advisor_user_id=advisor.id, client_user_id=client.id, account_id=account.id,
        simulated_date=account.simulated_date, summary=summary,
        metrics_json=json.dumps(metrics.model_dump()), recommendations_json=json.dumps(recommendations),
    )
    db.add(report)
    db.flush()
    return build_advisor_report_response(report)


def get_advisor_report_by_id(db: Session, report_id: int) -> AdvisorReportResponse:
    report = db.get(AdvisorReport, report_id)
    if report is None:
        raise RecordNotFoundError(f"No advisor report with id {report_id}")
    return build_advisor_report_response(report)


def build_advisor_report_response(report: AdvisorReport) -> AdvisorReportResponse:
    return AdvisorReportResponse(
        report_id=report.id, advisor_user_id=report.advisor_user_id,
        client_user_id=report.client_user_id, account_id=report.account_id,
        simulated_date=report.simulated_date, summary=report.summary,
        metrics=AdvisorMetricResponse(**json.loads(report.metrics_json)),
        recommendations=json.loads(report.recommendations_json), created_at=report.created_at,
    )
