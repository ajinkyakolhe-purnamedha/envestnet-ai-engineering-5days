"""YOU implement: memory (M9.2.5 — route on the effective question).

Yesterday's workflow routes on the bare question, so a follow-up like
"Why is that a problem for Alice?" loses the thread. Memory here is
just the transcript of past questions, windowed and prepended — the
router and the drafter see the conversation, not one orphaned turn.

The history holds the advisor's past QUESTIONS only, and never refused
ones (the chat panel guarantees both). Storing answer text too has a
failure mode worth remembering: notes contain words like "guidelines",
which would hijack the keyword router on every later turn.
"""

from sqlalchemy.orm import Session

from chronos.shared_database.api_schemas import (
    AdvisorAssistantAnswerResponse,
)

from labs.m9_advisor_assistant.m8_reference_assistant import (
    answer_client_question_for_m9,
)
from labs.m9_advisor_assistant.condense_conversation_history import (
    condense_conversation_history,
)


def answer_with_memory(
    db: Session,
    client_user_id: int,
    question: str,
    conversation_history: list[str] | None = None,
) -> AdvisorAssistantAnswerResponse:
    """Answer with the conversation in view, not just the last turn.

    Hints:
    - window first: condense_conversation_history(conversation_history
      or []) — keep the module-level import above, the tests patch it
      by name
    - build the effective question: the windowed turns and the new
      question joined with spaces (new question LAST — most recent
      wins); with no history the question passes through unchanged
    - hand the effective question to answer_client_question_for_m9 as
      its question, with the windowed history as conversation_history
    - safety comes free: a trade word in the NEW turn makes the
      effective question route to "trade", so refusals still fire
    """
    raise NotImplementedError("M9 lab step 3: wire the memory seam")
