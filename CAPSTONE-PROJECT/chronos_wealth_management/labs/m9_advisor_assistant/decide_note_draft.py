"""YOU implement: the human decision (M9.3.6 — the top verification rung).

The advisor approves or rejects, with a reason. This function is the
ONLY code in the whole app allowed to set an approved status — the
choke point that makes "nothing client-facing without a human" a
property of the system instead of a policy document.
"""

from sqlalchemy.orm import Session

from chronos.shared_database.api_schemas import AdvisorNoteDraftResponse
from chronos.shared_database.database_tables import AdvisorNoteDraft
from chronos.shared_database.domain_errors import (
    NoteDraftAlreadyDecidedError,
    RecordNotFoundError,
)

from labs.m9_advisor_assistant.note_draft_queries import (
    APPROVED_STATUS,
    PENDING_STATUS,
    REJECTED_STATUS,
    build_note_draft_response,
)


def decide_note_draft(
    db: Session,
    advisor_user_id: int,
    draft_id: int,
    decision: str,
    reason: str,
) -> AdvisorNoteDraftResponse:
    """Apply a final approve/reject decision to a pending draft.

    Hints:
    - db.get(AdvisorNoteDraft, draft_id); None ->
      RecordNotFoundError(f"No note draft with id {draft_id}")
    - a draft whose status is not PENDING_STATUS ->
      NoteDraftAlreadyDecidedError (decisions are final; there is no
      un-approve)
    - decision arrives validated as "approved" or "rejected" (the API
      schema enforces it); set status and decision_reason accordingly
    - db.flush(); return build_note_draft_response(draft)
    """
    raise NotImplementedError("M9 lab step 2: apply the human decision")
