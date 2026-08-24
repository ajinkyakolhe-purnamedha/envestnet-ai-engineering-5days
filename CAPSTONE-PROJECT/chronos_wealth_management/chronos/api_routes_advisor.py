"""Advisor workspace, report, and client communication routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from chronos.advisor_analysis_reports_and_client_lists import (
    generate_advisor_review_report,
    get_advisor_report_by_id,
    list_clients_for_advisor,
)
from chronos.advisor_assistant_runtime import (
    answer_advisor_question,
    decide_advisor_note_draft,
    judge_advisor_note,
    list_approved_advisor_notes,
    list_pending_advisor_note_drafts,
    submit_advisor_note_for_approval,
)
from chronos.api_routes.http_error_translation import translate_domain_errors
from chronos.demo_users.demo_user_login import get_demo_user_by_id
from chronos.demo_users.user_role_permissions import (
    require_advisor_user,
    require_investor_user,
)
from chronos.investor_accounts_portfolios_and_history import (
    build_current_portfolio_snapshot,
    get_account_for_investor_user,
)
from chronos.shared_database.api_schemas import (
    AdvisorAssistantAnswerResponse,
    AdvisorAssistantAskRequest,
    AdvisorClientSummaryResponse,
    AdvisorNoteDraftResponse,
    AdvisorReportResponse,
    ClientAdvisorMessageResponse,
    NoteDraftDecisionRequest,
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
    with translate_domain_errors():
        require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
        require_investor_user(get_demo_user_by_id(db, client_user_id))
        answer = answer_advisor_question(
            db, client_user_id, request.question, request.conversation_history
        )

        if answer.route != "portfolio" or answer.refused:
            return answer

        judge_verdict = judge_advisor_note(answer.note, answer.verdict)
        draft = submit_advisor_note_for_approval(
            db,
            advisor_user_id,
            client_user_id,
            request.question,
            answer,
            judge_verdict=judge_verdict,
        )
        return answer.model_copy(
            update={"judge_verdict": judge_verdict, "draft_id": draft.draft_id}
        )


@router.get("/advisor/drafts", response_model=list[AdvisorNoteDraftResponse])
def read_pending_note_drafts(
    advisor_user_id: int, db: Session = Depends(get_database_session)
):
    with translate_domain_errors():
        require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
        return list_pending_advisor_note_drafts(db, advisor_user_id)


@router.post(
    "/advisor/drafts/{draft_id}/decision",
    response_model=AdvisorNoteDraftResponse,
)
def decide_note_draft_route(
    draft_id: int,
    advisor_user_id: int,
    request: NoteDraftDecisionRequest,
    db: Session = Depends(get_database_session),
):
    with translate_domain_errors():
        require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
        return decide_advisor_note_draft(
            db, advisor_user_id, draft_id, request.decision, request.reason
        )


@router.get("/messages", response_model=list[ClientAdvisorMessageResponse])
def read_client_advisor_messages(
    user_id: int, db: Session = Depends(get_database_session)
):
    with translate_domain_errors():
        require_investor_user(get_demo_user_by_id(db, user_id))
        return list_approved_advisor_notes(db, user_id)


@router.get("/advisor/reports/{report_id}", response_model=AdvisorReportResponse)
def read_advisor_report(
    report_id: int,
    advisor_user_id: int,
    db: Session = Depends(get_database_session),
):
    with translate_domain_errors():
        require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
        return get_advisor_report_by_id(db, report_id)
