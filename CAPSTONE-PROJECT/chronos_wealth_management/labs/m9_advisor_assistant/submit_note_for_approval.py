"""YOU implement: the gate's intake (M9.4.1 — a draft is a row).

Nothing the assistant writes goes to a client directly. Every portfolio
answer becomes a PENDING row in advisor_note_drafts, waiting for a
human. Persistence comes free: a row survives a restart; a variable
does not.
"""

import json

from sqlalchemy.orm import Session

from chronos.investor_accounts.get_investor_account import (
    get_account_for_investor_user,
)
from chronos.shared_database.api_schemas import (
    AdvisorAssistantAnswerResponse,
    AdvisorNoteDraftResponse,
)
from chronos.shared_database.database_tables import AdvisorNoteDraft

from labs.m9_advisor_assistant.note_draft_queries import (
    PENDING_STATUS,
    build_note_draft_response,
)


def submit_note_for_approval(
    db: Session,
    advisor_user_id: int,
    client_user_id: int,
    question: str,
    answer: AdvisorAssistantAnswerResponse,
    judge_verdict: str | None = None,
) -> AdvisorNoteDraftResponse:
    """Persist the answer as a pending draft; return its response schema.

    Hints:
    - build an AdvisorNoteDraft row from the answer fields; store
      review_problems as JSON (json.dumps) in review_problems_json
    - status is ALWAYS PENDING_STATUS here — only decide_note_draft may
      ever set anything else
    - created_simulated_date comes from the client's account
      (get_account_for_investor_user(db, client_user_id).simulated_date)
      — the app's clock, not the wall clock
    - db.add(row); db.flush() — the session owner commits, you don't
    - return build_note_draft_response(row)
    """
    raise NotImplementedError("M9 lab step 1: persist the pending draft")
