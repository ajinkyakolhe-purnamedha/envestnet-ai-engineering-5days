"""Progress meter for the M1 advisor preview lab."""

from labs.m1_advisor_preview.build_preview_messages import (
    PREVIEW_INSTRUCTION,
    build_preview_messages,
)
from labs.m1_advisor_preview.draft_portfolio_preview import (
    TEMPLATE_SOURCE,
    draft_portfolio_preview,
)
from chronos.advisor_workspace.analyze_client_portfolio import (
    analyze_client_portfolio,
)
from chronos.investor_accounts.get_investor_account import (
    get_account_for_investor_user,
)
from chronos.portfolio_performance.calculate_current_portfolio_value import (
    build_current_portfolio_snapshot,
)


def test_preview_messages_label_instruction_context_and_question():
    messages = build_preview_messages("AAPL is 52%.", "What is the risk?", [])
    assert messages[0] == {"role": "system", "content": PREVIEW_INSTRUCTION}
    assert messages[-1]["role"] == "user"
    assert "CONTEXT:" in messages[-1]["content"]
    assert "QUESTION:" in messages[-1]["content"]


def test_previous_questions_become_user_turns():
    messages = build_preview_messages("facts", "follow-up", ["first question"])
    assert messages[1] == {"role": "user", "content": "first question"}


def test_template_preview_is_grounded_in_supplied_facts(db, alice):
    note, source = draft_portfolio_preview(db, alice.id, "How is the book?")
    account = get_account_for_investor_user(db, alice.id)
    portfolio = build_current_portfolio_snapshot(db, account)
    metrics = analyze_client_portfolio(portfolio)
    assert source == TEMPLATE_SOURCE
    assert f"{metrics.total_value:,.2f}"[:4] in note.replace(",", "")
    assert f"{metrics.cash_ratio:.0%}" in note or str(round(metrics.cash_ratio, 2)) in note


def test_preview_route_returns_501_until_lab_is_complete(client, db, alice, advisor):
    response = client.post(
        f"/advisor/clients/{alice.id}/preview",
        params={"advisor_user_id": advisor.id},
        json={"question": "How is this portfolio positioned?"},
    )
    if response.status_code == 501:
        return
    body = response.json()
    assert body["note"]
    assert body["note_source"] in {"template", "language_model"}


def test_preview_route_returns_note_when_lab_is_complete(client, db, alice, advisor):
    response = client.post(
        f"/advisor/clients/{alice.id}/preview",
        params={"advisor_user_id": advisor.id},
        json={"question": "How is this portfolio positioned?"},
    )
    assert response.status_code == 200
    assert response.json()["note_source"] == TEMPLATE_SOURCE
