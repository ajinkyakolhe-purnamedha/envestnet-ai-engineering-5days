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
from chronos.investor_accounts_portfolios_and_history import (
    get_account_for_investor_user,
    build_current_portfolio_snapshot,
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
    # The M8/M9 lab feature: this endpoint serves the participant-built
    # workflow in labs/ and answers 501 until the lab stubs are
    # implemented. The M9 additions degrade gracefully: until the M9
    # stubs exist, answers still flow — draft_id and judge_verdict stay
    # null and nothing enters the approval queue.
    from labs.m8_advisor_assistant.answer_client_question import (
        answer_client_question,
    )

    with translate_domain_errors():
        require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
        require_investor_user(get_demo_user_by_id(db, client_user_id))
        try:
            if request.conversation_history:
                from labs.m9_advisor_assistant.answer_with_memory import (
                    answer_with_memory,
                )

                answer = answer_with_memory(
                    db,
                    client_user_id,
                    request.question,
                    request.conversation_history,
                )
            else:
                try:
                    answer = answer_client_question(
                        db, client_user_id, request.question
                    )
                except NotImplementedError:
                    from labs.m9_advisor_assistant.m8_reference_assistant import (
                        answer_client_question_for_m9,
                    )

                    answer = answer_client_question_for_m9(
                        db, client_user_id, request.question
                    )
        except NotImplementedError as unfinished_lab_step:
            raise HTTPException(
                status_code=501,
                detail=(
                    "Advisor assistant not built yet — complete the "
                    f"lab: {unfinished_lab_step}"
                ),
            )

        if answer.route != "portfolio" or answer.refused:
            return answer

        judge_verdict = None
        try:
            from labs.m9_advisor_assistant.judge_note_with_model import (
                judge_note_with_model,
            )

            judge_verdict = judge_note_with_model(answer.note, answer.verdict)
        except NotImplementedError:
            judge_verdict = None

        draft_id = None
        try:
            from labs.m9_advisor_assistant.submit_note_for_approval import (
                submit_note_for_approval,
            )

            draft = submit_note_for_approval(
                db,
                advisor_user_id,
                client_user_id,
                request.question,
                answer,
                judge_verdict=judge_verdict,
            )
            draft_id = draft.draft_id
        except NotImplementedError:
            draft_id = None

        return answer.model_copy(
            update={"judge_verdict": judge_verdict, "draft_id": draft_id}
        )


@router.get(
    "/advisor/drafts", response_model=list[AdvisorNoteDraftResponse]
)
def read_pending_note_drafts(
    advisor_user_id: int, db: Session = Depends(get_database_session)
):
    # M9 lab: the approval queue. The query is given, so this endpoint
    # works from day one — it simply stays empty until the lab's submit
    # step starts queueing drafts.
    from labs.m9_advisor_assistant.note_draft_queries import (
        list_pending_drafts_for_advisor,
    )

    with translate_domain_errors():
        require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
        return list_pending_drafts_for_advisor(db, advisor_user_id)


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
    # M9 lab: the human gate. 501 until decide_note_draft is written —
    # the Approve button on the dashboard literally does not work until
    # a human decision function exists.
    from labs.m9_advisor_assistant.decide_note_draft import (
        decide_note_draft,
    )

    with translate_domain_errors():
        require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
        try:
            return decide_note_draft(
                db,
                advisor_user_id,
                draft_id,
                request.decision,
                request.reason,
            )
        except NotImplementedError as unfinished_lab_step:
            raise HTTPException(
                status_code=501,
                detail=(
                    "Approval gate not built yet — complete the "
                    f"lab: {unfinished_lab_step}"
                ),
            )


@router.get("/messages", response_model=list[ClientAdvisorMessageResponse])
def read_client_advisor_messages(
    user_id: int, db: Session = Depends(get_database_session)
):
    # M9 lab: the investor-facing side of the gate. Approved notes only,
    # enforced by the given query — a rejected or pending draft can
    # never appear here.
    from labs.m9_advisor_assistant.note_draft_queries import (
        list_approved_notes_for_client,
    )

    with translate_domain_errors():
        require_investor_user(get_demo_user_by_id(db, user_id))
        return list_approved_notes_for_client(db, user_id)


@router.get("/advisor/reports/{report_id}", response_model=AdvisorReportResponse)
def read_advisor_report(
    report_id: int,
    advisor_user_id: int,
    db: Session = Depends(get_database_session),
):
    with translate_domain_errors():
        require_advisor_user(get_demo_user_by_id(db, advisor_user_id))
        return get_advisor_report_by_id(db, report_id)
