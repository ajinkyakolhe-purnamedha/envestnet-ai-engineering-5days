"""Deterministic advisor review report, persisted to advisor_reports."""

import json

from sqlalchemy.orm import Session

from chronos.advisor_workspace.analyze_client_portfolio import (
    analyze_client_portfolio,
    build_advisor_recommendations,
)
from chronos.demo_users.demo_user_login import get_demo_user_by_id
from chronos.demo_users.user_role_permissions import (
    require_advisor_user,
    require_investor_user,
)
from chronos.investor_accounts.get_investor_account import (
    get_account_for_investor_user,
)
from chronos.portfolio_performance.calculate_current_portfolio_value import (
    build_current_portfolio_snapshot,
)
from chronos.shared_database.api_schemas import (
    AdvisorMetricResponse,
    AdvisorReportResponse,
)
from chronos.shared_database.database_tables import AdvisorReport
from chronos.shared_database.domain_errors import RecordNotFoundError


def generate_advisor_review_report(
    db: Session, advisor_user_id: int, client_user_id: int
) -> AdvisorReportResponse:
    advisor = get_demo_user_by_id(db, advisor_user_id)
    require_advisor_user(advisor)
    client = get_demo_user_by_id(db, client_user_id)
    require_investor_user(client)

    account = get_account_for_investor_user(db, client.id)
    portfolio = build_current_portfolio_snapshot(db, account)
    metrics = analyze_client_portfolio(portfolio)
    recommendations = build_advisor_recommendations(portfolio)

    summary = (
        f"As of {account.simulated_date}, {client.name}'s portfolio is worth "
        f"${metrics.total_value:,.2f} ({metrics.total_return_percentage:+.2f}% "
        f"total return) across {metrics.number_of_holdings} holdings, with "
        f"{len(recommendations)} advisory flags."
    )

    report = AdvisorReport(
        advisor_user_id=advisor.id,
        client_user_id=client.id,
        account_id=account.id,
        simulated_date=account.simulated_date,
        summary=summary,
        metrics_json=json.dumps(metrics.model_dump()),
        recommendations_json=json.dumps(recommendations),
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
        report_id=report.id,
        advisor_user_id=report.advisor_user_id,
        client_user_id=report.client_user_id,
        account_id=report.account_id,
        simulated_date=report.simulated_date,
        summary=report.summary,
        metrics=AdvisorMetricResponse(**json.loads(report.metrics_json)),
        recommendations=json.loads(report.recommendations_json),
        created_at=report.created_at,
    )
