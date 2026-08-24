"""Your progress meter. Run constantly, make it green file by file:

    uv run python -m pytest labs/m8_advisor_assistant -q

Tests are ordered by build step. Everything runs offline on the
template path — no model, no key, no network required.
"""

import pytest

from labs.m8_advisor_assistant.answer_client_question import (
    answer_client_question,
)
from labs.m8_advisor_assistant.draft_advisor_note import (
    TEMPLATE_SOURCE,
    draft_advisor_note,
)
from labs.m8_advisor_assistant.judge_against_guidelines import (
    judge_against_guidelines,
)
from labs.m8_advisor_assistant.review_advisor_note import review_advisor_note
from labs.m8_advisor_assistant.route_client_question import (
    route_client_question,
)
from chronos.advisor_analysis_reports_and_client_lists import (
    analyze_client_portfolio,
)
from chronos.investor_accounts_portfolios_and_history import (
    build_current_portfolio_snapshot,
    get_account_for_investor_user,
)


# -- step 1: the router ------------------------------------------------


def test_portfolio_questions_route_to_portfolio():
    assert route_client_question("How is Alice's portfolio doing?") == "portfolio"


def test_policy_questions_route_to_policy():
    assert route_client_question("What does the guideline say?") == "policy"


@pytest.mark.parametrize(
    "question",
    [
        "Buy 100 shares of AAPL now.",
        "Please liquidate the account.",
        "How much cash would selling AAPL raise?",
        "Dump the Apple shares.",
    ],
)
def test_trade_shaped_questions_are_recognized(question):
    assert route_client_question(question) == "trade"


# -- step 3: the verdict -----------------------------------------------


def test_verdict_matches_portfolio_analysis(db, alice):
    account = get_account_for_investor_user(db, alice.id)
    portfolio = build_current_portfolio_snapshot(db, account)
    metrics = analyze_client_portfolio(portfolio)
    verdict = judge_against_guidelines(metrics)
    breached = (
        metrics.largest_position_ratio > 0.35 or metrics.cash_ratio > 0.40
    )
    assert ("outside guidelines" in verdict) == breached


# -- step 4: the draft (template path) ---------------------------------


def test_template_note_is_deterministic_and_grounded(db, alice):
    account = get_account_for_investor_user(db, alice.id)
    portfolio = build_current_portfolio_snapshot(db, account)
    metrics = analyze_client_portfolio(portfolio)
    verdict = judge_against_guidelines(metrics)
    note, source = draft_advisor_note("How is it going?", metrics, verdict, [])
    assert source == TEMPLATE_SOURCE
    assert note == draft_advisor_note("How is it going?", metrics, verdict, [])[0]


# -- step 5: the evaluator gate ----------------------------------------


def test_bad_note_fails_both_rules():
    problems = review_advisor_note(
        "word " * 90,
        "outside guidelines: AAPL is 36% of the portfolio, above the "
        "35% concentration limit",
    )
    assert any("35" in p for p in problems)
    assert any("word" in p.lower() or "long" in p.lower() for p in problems)


def test_good_note_passes():
    assert (
        review_advisor_note(
            "AAPL breaches the 35% concentration limit.",
            "outside guidelines: above the 35% concentration limit",
        )
        == []
    )


# -- step 6: the workflow ----------------------------------------------


def test_trade_question_is_refused_without_touching_data(db, alice):
    answer = answer_client_question(db, alice.id, "Sell everything today.")
    assert answer.refused is True
    assert answer.metrics is None


def test_portfolio_question_returns_grounded_note(db, alice):
    answer = answer_client_question(
        db, alice.id, "How is this client's portfolio positioned?"
    )
    assert answer.refused is False
    assert answer.metrics is not None
    assert answer.verdict is not None
    assert answer.note_source == TEMPLATE_SOURCE
    assert answer.review_problems == []


def test_policy_question_needs_no_client_data(db, alice):
    answer = answer_client_question(db, alice.id, "What is the policy limit?")
    assert answer.refused is False
    assert answer.metrics is None
    assert "35%" in answer.note


# -- step 7: your workflow, served by the API --------------------------


def test_advisor_gets_an_answer_over_http(client, db, alice, advisor):
    response = client.post(
        f"/advisor/clients/{alice.id}/assistant",
        params={"advisor_user_id": advisor.id},
        json={"question": "How is this portfolio positioned?"},
    )
    assert response.status_code == 200  # 501 = lab not finished
    body = response.json()
    assert body["route"] == "portfolio"
    assert body["refused"] is False
    assert body["metrics"] is not None


def test_trade_request_is_refused_over_http(client, db, alice, advisor):
    response = client.post(
        f"/advisor/clients/{alice.id}/assistant",
        params={"advisor_user_id": advisor.id},
        json={"question": "Buy more AAPL for this client."},
    )
    assert response.status_code == 200
    assert response.json()["refused"] is True
