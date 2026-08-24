"""YOU implement: the workflow (M8.2.8 — least autonomy that works).

Assemble your five pieces. No agent loop, no planner: the steps are
known, so Python orders them and the model only writes prose.
"""

from sqlalchemy.orm import Session

from chronos.api_schemas_advisor import (
    AdvisorAssistantAnswerResponse,
)

from labs.m8_advisor_assistant.draft_advisor_note import (
    TEMPLATE_SOURCE,
    draft_advisor_note,
)
from labs.m8_advisor_assistant.gather_client_facts import gather_client_facts
from labs.m8_advisor_assistant.judge_against_guidelines import (
    judge_against_guidelines,
)
from labs.m8_advisor_assistant.review_advisor_note import review_advisor_note
from labs.m8_advisor_assistant.route_client_question import (
    POLICY_ROUTE,
    TRADE_ROUTE,
    route_client_question,
)


def answer_client_question(
    db: Session,
    client_user_id: int,
    question: str,
    conversation_history: list[str] | None = None,
) -> AdvisorAssistantAnswerResponse:
    """Route, then refuse / explain / gather-judge-draft-review.

    Required behavior:
    - "trade"  -> refused=True, metrics=None, note explains why,
      and NOTHING was gathered (no data access on refusals)
    - "policy" -> answer from the two thresholds, no client data
    - "portfolio" -> gather -> judge -> draft -> review; if the review
      finds problems, redraft ONCE (pass revision_problems), re-review,
      and ship with any remaining problems attached
    - conversation_history is accepted and ignored — M9's memory seam

    Response fields: route, refused, verdict, note, note_source,
    review_problems, metrics.
    """
    raise NotImplementedError("M8 lab step 6: assemble the workflow")
