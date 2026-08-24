"""Stable, route-facing runtime for the advisor-assistant workflow.

The teaching labs remain independently runnable exercises.  This module is
the application seam: it always provides the deterministic reference behavior
and owns the API workflow's draft and approval operations.
"""

from collections.abc import Callable

from sqlalchemy.orm import Session

from chronos.advisor_assistant_drafts_and_approval import (
    answer_client_question_for_m9,
    answer_with_memory,
    decide_note_draft,
    list_approved_notes_for_client,
    list_pending_drafts_for_advisor,
    submit_note_for_approval,
)
from chronos.shared_database.api_schemas import (
    AdvisorAssistantAnswerResponse,
    AdvisorNoteDraftResponse,
    ClientAdvisorMessageResponse,
)

Judge = Callable[[str, str | None], str | None]


def answer_advisor_question(
    db: Session,
    client_user_id: int,
    question: str,
    conversation_history: list[str] | None = None,
) -> AdvisorAssistantAnswerResponse:
    """Answer through the deterministic runtime, optionally retaining context."""
    if conversation_history:
        return answer_with_memory(db, client_user_id, question, conversation_history)
    return answer_client_question_for_m9(db, client_user_id, question)


def judge_advisor_note(
    note: str, verdict: str | None, judge: Judge | None = None
) -> str | None:
    """Return an advisory judge result when a runtime judge is configured."""
    if judge is None:
        return None
    try:
        return judge(note, verdict)
    except NotImplementedError:
        return None


def submit_advisor_note_for_approval(
    db: Session,
    advisor_user_id: int,
    client_user_id: int,
    question: str,
    answer: AdvisorAssistantAnswerResponse,
    judge_verdict: str | None = None,
) -> AdvisorNoteDraftResponse:
    """Queue a portfolio answer for the mandatory human approval gate."""
    return submit_note_for_approval(
        db, advisor_user_id, client_user_id, question, answer, judge_verdict
    )


def decide_advisor_note_draft(
    db: Session,
    advisor_user_id: int,
    draft_id: int,
    decision: str,
    reason: str,
) -> AdvisorNoteDraftResponse:
    """Record the advisor's final approval or rejection."""
    return decide_note_draft(db, advisor_user_id, draft_id, decision, reason)


def list_pending_advisor_note_drafts(
    db: Session, advisor_user_id: int
) -> list[AdvisorNoteDraftResponse]:
    return list_pending_drafts_for_advisor(db, advisor_user_id)


def list_approved_advisor_notes(
    db: Session, client_user_id: int
) -> list[ClientAdvisorMessageResponse]:
    return list_approved_notes_for_client(db, client_user_id)
