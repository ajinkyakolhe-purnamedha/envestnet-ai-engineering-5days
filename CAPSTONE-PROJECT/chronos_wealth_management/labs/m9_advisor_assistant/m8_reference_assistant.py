"""GIVEN: a compact M8 stand-in so M9 can run independently.

This is not the M8 answer key. It is the smallest deterministic
assistant M9 needs: route/refuse, answer policy questions, and produce
a grounded portfolio draft from Chronos read-only facts. Participants
can swap in their own M8 implementation as a stretch after M9 is green.
"""

from sqlalchemy.orm import Session

from chronos.advisor_workspace.analyze_client_portfolio import (
    CONCENTRATION_THRESHOLD,
    HIGH_CASH_THRESHOLD,
    analyze_client_portfolio,
    build_advisor_recommendations,
)
from chronos.investor_accounts.get_investor_account import (
    get_account_for_investor_user,
)
from chronos.portfolio_performance.calculate_current_portfolio_value import (
    build_current_portfolio_snapshot,
)
from chronos.shared_database.api_schemas import AdvisorAssistantAnswerResponse

TRADE_ROUTE = "trade"
POLICY_ROUTE = "policy"
PORTFOLIO_ROUTE = "portfolio"

_TRADE_WORDS = ("buy", "sell", "liquidate", "dump", "cash out", "trade")
_POLICY_WORDS = ("policy", "guideline", "rule", "threshold", "limit")


def answer_client_question_for_m9(
    db: Session,
    client_user_id: int,
    question: str,
    conversation_history: list[str] | None = None,
) -> AdvisorAssistantAnswerResponse:
    """Return a deterministic M8-shaped answer for the M9 lab."""
    route = _route_reference_question(question)
    if route == TRADE_ROUTE:
        return AdvisorAssistantAnswerResponse(
            route=TRADE_ROUTE,
            refused=True,
            verdict=None,
            note="Refused: the advisor assistant drafts notes only and cannot trade.",
            note_source="m9_reference",
            review_problems=[],
            metrics=None,
        )

    if route == POLICY_ROUTE:
        return AdvisorAssistantAnswerResponse(
            route=POLICY_ROUTE,
            refused=False,
            verdict=None,
            note=(
                f"Policy: single positions should stay at or below "
                f"{CONCENTRATION_THRESHOLD:.0%}; cash should stay at or "
                f"below {HIGH_CASH_THRESHOLD:.0%}."
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
    note = _build_reference_note(metrics, verdict, recommendations)
    return AdvisorAssistantAnswerResponse(
        route=PORTFOLIO_ROUTE,
        refused=False,
        verdict=verdict,
        note=note,
        note_source="m9_reference",
        review_problems=[],
        metrics=metrics,
    )


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
            "outside guidelines: "
            f"{metrics.largest_position_symbol} is "
            f"{metrics.largest_position_ratio:.0%} of the portfolio "
            f"(limit {CONCENTRATION_THRESHOLD:.0%})"
        )
    if metrics.cash_ratio > HIGH_CASH_THRESHOLD:
        return (
            "outside guidelines: cash is "
            f"{metrics.cash_ratio:.0%} of the portfolio "
            f"(limit {HIGH_CASH_THRESHOLD:.0%})"
        )
    return "within guidelines"


def _build_reference_note(metrics, verdict: str, recommendations: list[str]) -> str:
    if recommendations:
        first_recommendation = recommendations[0]
    else:
        first_recommendation = "No advisory flags are present."
    return (
        f"Portfolio value is ${metrics.total_value:,.2f}, with "
        f"{metrics.cash_ratio:.0%} in cash and "
        f"{metrics.number_of_holdings} holdings. Verdict: {verdict}. "
        f"{first_recommendation}"
    )
