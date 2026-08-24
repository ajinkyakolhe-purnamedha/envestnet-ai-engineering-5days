"""YOU implement: draft a portfolio explanation preview (M1)."""

from sqlalchemy.orm import Session

from labs.m1_advisor_preview.build_preview_messages import build_preview_messages
from labs.m1_advisor_preview.call_preview_model import call_preview_model
from labs.m1_advisor_preview.gather_preview_facts import gather_preview_facts

LANGUAGE_MODEL_SOURCE = "language_model"
TEMPLATE_SOURCE = "template"


def draft_portfolio_preview(
    db: Session,
    client_user_id: int,
    question: str,
    previous_questions: list[str] | None = None,
) -> tuple[str, str]:
    """Return (note, note_source).

    Hints:
    - gather metrics and recommendations with gather_preview_facts
    - build a context string that includes total_value, cash_ratio, and each
      recommendation on its own line
    - messages = build_preview_messages(context, question, previous_questions or [])
    - answer = call_preview_model(messages); when None, build a template note
      that cites total_value, cash_ratio, and every recommendation, then return
      TEMPLATE_SOURCE
    """
    raise NotImplementedError("M1 lab step 3: draft the portfolio preview")
