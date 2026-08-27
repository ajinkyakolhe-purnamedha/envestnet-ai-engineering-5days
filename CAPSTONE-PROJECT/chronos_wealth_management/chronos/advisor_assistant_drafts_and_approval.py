"""Production owner for advisor-assistant drafts, memory, and human approval.

The runtime module owns the route-facing assistant loop; this module owns the
durable draft and approval state it uses.
"""

import json

from sqlalchemy.orm import Session

from chronos.advisor_analysis_reports_and_client_lists import (
    CONCENTRATION_THRESHOLD,
    HIGH_CASH_THRESHOLD,
    analyze_client_portfolio,
    build_advisor_recommendations,
)
from chronos.investor_accounts_portfolios_and_history import (
    build_current_portfolio_snapshot,
    get_account_for_investor_user,
)
from chronos.api_schemas_advisor import (
    AdvisorAssistantAnswerResponse,
    AdvisorNoteDraftResponse,
    ClientAdvisorMessageResponse,
)
from chronos.application_database import AdvisorNoteDraft
from chronos.application_errors_and_permissions import (
    NoteDraftAlreadyDecidedError,
    RecordNotFoundError,
)

PENDING_STATUS = "pending"
APPROVED_STATUS = "approved"
REJECTED_STATUS = "rejected"
TRADE_ROUTE = "trade"
POLICY_ROUTE = "policy"
PORTFOLIO_ROUTE = "portfolio"
_TRADE_WORDS = ("buy", "sell", "liquidate", "dump", "cash out", "trade")
_POLICY_WORDS = ("policy", "guideline", "rule", "threshold", "limit")


def build_note_draft_response(draft: AdvisorNoteDraft) -> AdvisorNoteDraftResponse:
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


def submit_note_for_approval(
    db: Session,
    advisor_user_id: int,
    client_user_id: int,
    question: str,
    answer: AdvisorAssistantAnswerResponse,
    judge_verdict: str | None = None,
) -> AdvisorNoteDraftResponse:
    account = get_account_for_investor_user(db, client_user_id)
    draft = AdvisorNoteDraft(
        advisor_user_id=advisor_user_id,
        client_user_id=client_user_id,
        question=question,
        note=answer.note,
        verdict=answer.verdict,
        note_source=answer.note_source,
        review_problems_json=json.dumps(answer.review_problems),
        judge_verdict=judge_verdict,
        status=PENDING_STATUS,
        created_simulated_date=account.simulated_date,
    )
    db.add(draft)
    db.flush()
    return build_note_draft_response(draft)


def decide_note_draft(
    db: Session,
    advisor_user_id: int,
    draft_id: int,
    decision: str,
    reason: str,
) -> AdvisorNoteDraftResponse:
    draft = db.get(AdvisorNoteDraft, draft_id)
    if draft is None:
        raise RecordNotFoundError(f"No note draft with id {draft_id}")
    if draft.advisor_user_id != advisor_user_id:
        raise RecordNotFoundError(f"No note draft with id {draft_id}")
    if draft.status != PENDING_STATUS:
        raise NoteDraftAlreadyDecidedError(f"Note draft {draft_id} was already decided")
    draft.status = decision
    draft.decision_reason = reason
    db.flush()
    return build_note_draft_response(draft)


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


def answer_client_question_for_m9(
    db: Session,
    client_user_id: int,
    question: str,
    conversation_history: list[str] | None = None,
) -> AdvisorAssistantAnswerResponse:
    route = _route_reference_question(question)
    if route == TRADE_ROUTE:
        return AdvisorAssistantAnswerResponse(
            route=route,
            refused=True,
            verdict=None,
            note="Refused: the advisor assistant drafts notes only and cannot trade.",
            note_source="m9_reference",
            review_problems=[],
            metrics=None,
        )
    if route == POLICY_ROUTE:
        return AdvisorAssistantAnswerResponse(
            route=route,
            refused=False,
            verdict=None,
            note=(
                f"Policy: single positions should stay at or below "
                f"{CONCENTRATION_THRESHOLD:.0%}; cash should stay at or below "
                f"{HIGH_CASH_THRESHOLD:.0%}."
            ),
            note_source="m9_reference",
            review_problems=[],
            metrics=None,
        )
    account = get_account_for_investor_user(db, client_user_id)
    portfolio = build_current_portfolio_snapshot(db, account)
    metrics = analyze_client_portfolio(portfolio)
    recommendations = build_advisor_recommendations(portfolio)
    verdict = _build_reference_verdict(metrics)
    first_recommendation = (
        recommendations[0] if recommendations else "No advisory flags are present."
    )
    return AdvisorAssistantAnswerResponse(
        route=route,
        refused=False,
        verdict=verdict,
        note=(
            f"Portfolio value is ${metrics.total_value:,.2f}, with "
            f"{metrics.cash_ratio:.0%} in cash and {metrics.number_of_holdings} "
            f"holdings. Verdict: {verdict}. {first_recommendation}"
        ),
        note_source="m9_reference",
        review_problems=[],
        metrics=metrics,
    )


def answer_with_memory(
    db: Session,
    client_user_id: int,
    question: str,
    conversation_history: list[str] | None = None,
) -> AdvisorAssistantAnswerResponse:
    history = condense_conversation_history(conversation_history or [])
    effective_question = " ".join([*history, question]) if history else question
    return answer_client_question_for_m9(db, client_user_id, effective_question, history)


def condense_conversation_history(
    history: list[str], recent_turns_to_keep: int = 4
) -> list[str]:
    if len(history) <= recent_turns_to_keep:
        return list(history)
    older_questions = " | ".join(turn[:60] for turn in history[:-recent_turns_to_keep])
    return ["Earlier questions: " + older_questions, *history[-recent_turns_to_keep:]]


def _route_reference_question(question: str) -> str:
    text = question.lower()
    if any(word in text for word in _TRADE_WORDS):
        return TRADE_ROUTE
    if any(word in text for word in _POLICY_WORDS):
        return POLICY_ROUTE
    return PORTFOLIO_ROUTE


def _build_reference_verdict(metrics) -> str:
    if metrics.largest_position_ratio > CONCENTRATION_THRESHOLD:
        return (
            f"outside guidelines: {metrics.largest_position_symbol} is "
            f"{metrics.largest_position_ratio:.0%} of the portfolio "
            f"(limit {CONCENTRATION_THRESHOLD:.0%})"
        )
    if metrics.cash_ratio > HIGH_CASH_THRESHOLD:
        return (
            f"outside guidelines: cash is {metrics.cash_ratio:.0%} of the "
            f"portfolio (limit {HIGH_CASH_THRESHOLD:.0%})"
        )
    return "within guidelines"
