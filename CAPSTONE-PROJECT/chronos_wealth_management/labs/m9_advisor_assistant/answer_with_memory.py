"""Compatibility seam for the M9 lab; production ownership is in chronos."""

from sqlalchemy.orm import Session

from chronos.advisor_assistant_drafts_and_approval import (
    answer_client_question_for_m9,
    condense_conversation_history,
)
from chronos.api_schemas_advisor import AdvisorAssistantAnswerResponse


def answer_with_memory(
    db: Session,
    client_user_id: int,
    question: str,
    conversation_history: list[str] | None = None,
) -> AdvisorAssistantAnswerResponse:
    """Delegate through patchable lab seams while keeping behavior production-owned."""
    history = condense_conversation_history(conversation_history or [])
    effective_question = " ".join([*history, question]) if history else question
    return answer_client_question_for_m9(
        db, client_user_id, effective_question, history
    )
