"""Advisor client list, client portfolio, and report routes — read only."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from chronos.advisor_workspace.generate_advisor_review_report import (
    generate_advisor_review_report,
    get_advisor_report_by_id,
)
from chronos.advisor_workspace.list_advisor_clients import list_clients_for_advisor
from chronos.api_routes.http_error_translation import translate_domain_errors
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
    AdvisorAssistantAnswerResponse,
    AdvisorAssistantAskRequest,
    AdvisorClientSummaryResponse,
    AdvisorReportResponse,
    PortfolioResponse,
)
from chronos.shared_database.database_connection import get_database_session

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


@router.post(
    "/advisor/clients/{client_user_id}/report", response_model=AdvisorReportResponse
)
def create_advisor_client_report(
    client_user_id: int,
    advisor_user_id: int,
    db: Session = Depends(get_database_session),
):
    with translate_domain_errors():
        return generate_advisor_review_report(db, advisor_user_id, client_user_id)


@router.post(
    "/advisor/clients/{client_user_id}/assistant",
    response_model=AdvisorAssistantAnswerResponse,
)
def ask_advisor_assistant(
    client_user_id: int,
    advisor_user_id: int,
    request: AdvisorAssistantAskRequest,
    db: Session = Depends(get_database_session),
):
    # The M8 lab feature: this endpoint serves the participant-built
    # workflow in labs/m8_advisor_assistant and answers 501 until the
    # lab stubs are implemented.
    from labs.m8_advisor_assistant.answer_client_question import (
        answer_client_question,
    )

    with translate_domain_errors():
        require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
        require_investor_user(get_demo_user_by_id(db, client_user_id))
        try:
            return answer_client_question(db, client_user_id, request.question)
        except NotImplementedError as unfinished_lab_step:
            raise HTTPException(
                status_code=501,
                detail=(
                    "Advisor assistant not built yet — complete the M8 "
                    f"lab: {unfinished_lab_step}"
                ),
            )


@router.get("/advisor/reports/{report_id}", response_model=AdvisorReportResponse)
def read_advisor_report(
    report_id: int,
    advisor_user_id: int,
    db: Session = Depends(get_database_session),
):
    with translate_domain_errors():
        require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
        return get_advisor_report_by_id(db, report_id)
