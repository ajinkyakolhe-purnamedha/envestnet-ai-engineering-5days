"""GIVEN: read-side queries and the row-to-response builder.

Your submit and decide functions write ``AdvisorNoteDraft`` rows; these
queries are how the two dashboards read them back. The visibility rule
lives here in one place: a client sees approved notes and nothing else.
"""

import json

from sqlalchemy.orm import Session

from chronos.shared_database.api_schemas import (
    AdvisorNoteDraftResponse,
    ClientAdvisorMessageResponse,
)
from chronos.shared_database.database_tables import AdvisorNoteDraft

PENDING_STATUS = "pending"
APPROVED_STATUS = "approved"
REJECTED_STATUS = "rejected"


def build_note_draft_response(
    draft: AdvisorNoteDraft,
) -> AdvisorNoteDraftResponse:
    return AdvisorNoteDraftResponse(
        draft_id=draft.id,
        advisor_user_id=draft.advisor_user_id,
        client_user_id=draft.client_user_id,
        question=draft.question,
        note=draft.note,
        verdict=draft.verdict,
        note_source=draft.note_source,
        review_problems=json.loads(draft.review_problems_json),
        judge_verdict=draft.judge_verdict,
        status=draft.status,
        decision_reason=draft.decision_reason,
        created_simulated_date=draft.created_simulated_date,
    )


def list_pending_drafts_for_advisor(
    db: Session, advisor_user_id: int
) -> list[AdvisorNoteDraftResponse]:
    drafts = (
        db.query(AdvisorNoteDraft)
        .filter(
            AdvisorNoteDraft.advisor_user_id == advisor_user_id,
            AdvisorNoteDraft.status == PENDING_STATUS,
        )
        .order_by(AdvisorNoteDraft.id)
        .all()
    )
    return [build_note_draft_response(draft) for draft in drafts]


def list_approved_notes_for_client(
    db: Session, client_user_id: int
) -> list[ClientAdvisorMessageResponse]:
    drafts = (
        db.query(AdvisorNoteDraft)
        .filter(
            AdvisorNoteDraft.client_user_id == client_user_id,
            AdvisorNoteDraft.status == APPROVED_STATUS,
        )
        .order_by(AdvisorNoteDraft.id)
        .all()
    )
    return [
        ClientAdvisorMessageResponse(
            draft_id=draft.id,
            note=draft.note,
            created_simulated_date=draft.created_simulated_date,
        )
        for draft in drafts
    ]
