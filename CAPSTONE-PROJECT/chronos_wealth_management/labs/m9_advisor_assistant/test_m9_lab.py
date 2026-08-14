"""Your progress meter. Run constantly, make it green step by step:

    uv run python -m pytest labs/m9_advisor_assistant -q

Ordered by build step: the gate first (tests 1-6), the payoff over HTTP
(7-10), memory (11-13), then the stretch judge (14-15, skipped until you
implement it). Everything runs offline on the template path, and M9 has
a compact reference assistant so these tests grade your M9 code only.
"""

import pytest

from chronos.shared_database.api_schemas import (
    AdvisorAssistantAnswerResponse,
)
from chronos.shared_database.database_tables import AdvisorNoteDraft
from chronos.shared_database.domain_errors import (
    NoteDraftAlreadyDecidedError,
)

from labs.m9_advisor_assistant import answer_with_memory as memory_module
from labs.m9_advisor_assistant import (
    judge_note_with_model as judge_module,
)
from labs.m9_advisor_assistant.answer_with_memory import answer_with_memory
from labs.m9_advisor_assistant.condense_conversation_history import (
    condense_conversation_history,
)
from labs.m9_advisor_assistant.decide_note_draft import decide_note_draft
from labs.m9_advisor_assistant.judge_note_with_model import (
    judge_note_with_model,
)
from labs.m9_advisor_assistant.note_draft_queries import (
    APPROVED_STATUS,
    PENDING_STATUS,
    REJECTED_STATUS,
    list_approved_notes_for_client,
    list_pending_drafts_for_advisor,
)
from labs.m9_advisor_assistant.submit_note_for_approval import (
    submit_note_for_approval,
)


def _sample_answer() -> AdvisorAssistantAnswerResponse:
    return AdvisorAssistantAnswerResponse(
        route="portfolio",
        refused=False,
        verdict="outside guidelines: AAPL is 52% of portfolio (limit 35%)",
        note="AAPL sits at 52% of the portfolio, above the 35% limit.",
        note_source="template",
        review_problems=["note is one word over the limit"],
        metrics=None,
    )


# -- step 1: submit — the gate's intake --------------------------------


def test_submit_creates_a_pending_row(db, advisor, alice):
    submit_note_for_approval(
        db, advisor.id, alice.id, "How concentrated is she?",
        _sample_answer(),
    )
    row = db.query(AdvisorNoteDraft).one()
    assert row.status == PENDING_STATUS


def test_submit_copies_the_answer_faithfully(db, advisor, alice,
                                             alice_account):
    answer = _sample_answer()
    draft = submit_note_for_approval(
        db, advisor.id, alice.id, "How concentrated is she?", answer,
        judge_verdict="NO",
    )
    assert draft.question == "How concentrated is she?"
    assert draft.note == answer.note
    assert draft.verdict == answer.verdict
    assert draft.note_source == answer.note_source
    assert draft.review_problems == answer.review_problems
    assert draft.judge_verdict == "NO"
    assert draft.created_simulated_date == alice_account.simulated_date


def test_submit_can_never_approve(db, advisor, alice):
    first = submit_note_for_approval(
        db, advisor.id, alice.id, "Q1", _sample_answer()
    )
    second = submit_note_for_approval(
        db, advisor.id, alice.id, "Q2", _sample_answer()
    )
    assert first.status == second.status == PENDING_STATUS
    assert list_approved_notes_for_client(db, alice.id) == []


# -- step 2: decide — the human gate -----------------------------------


def test_approve_sets_status_and_reason(db, advisor, alice):
    draft = submit_note_for_approval(
        db, advisor.id, alice.id, "Q", _sample_answer()
    )
    decided = decide_note_draft(
        db, advisor.id, draft.draft_id, APPROVED_STATUS,
        "Figures verified against the report.",
    )
    assert decided.status == APPROVED_STATUS
    assert decided.decision_reason == "Figures verified against the report."


def test_rejected_notes_never_reach_the_client(db, advisor, alice):
    kept = submit_note_for_approval(
        db, advisor.id, alice.id, "Q-keep", _sample_answer()
    )
    dropped = submit_note_for_approval(
        db, advisor.id, alice.id, "Q-drop", _sample_answer()
    )
    decide_note_draft(db, advisor.id, kept.draft_id, APPROVED_STATUS, "ok")
    decide_note_draft(
        db, advisor.id, dropped.draft_id, REJECTED_STATUS, "tone"
    )
    messages = list_approved_notes_for_client(db, alice.id)
    assert [message.draft_id for message in messages] == [kept.draft_id]
    assert list_pending_drafts_for_advisor(db, advisor.id) == []


def test_decisions_are_final(db, advisor, alice):
    draft = submit_note_for_approval(
        db, advisor.id, alice.id, "Q", _sample_answer()
    )
    decide_note_draft(db, advisor.id, draft.draft_id, REJECTED_STATUS, "no")
    with pytest.raises(NoteDraftAlreadyDecidedError):
        decide_note_draft(
            db, advisor.id, draft.draft_id, APPROVED_STATUS, "changed mind"
        )


# -- the payoff, over HTTP ---------------------------------------------


def test_assistant_endpoint_queues_a_draft(client, db, alice, advisor,
                                           canned_assistant):
    response = client.post(
        f"/advisor/clients/{alice.id}/assistant",
        params={"advisor_user_id": advisor.id},
        json={"question": "How is this portfolio positioned?"},
    )
    assert response.status_code == 200
    draft_id = response.json()["draft_id"]
    assert draft_id is not None
    queue = client.get(
        "/advisor/drafts", params={"advisor_user_id": advisor.id}
    ).json()
    assert [draft["draft_id"] for draft in queue] == [draft_id]
    assert queue[0]["status"] == PENDING_STATUS


def test_assistant_endpoint_uses_m9_reference_when_m8_is_unfinished(
    client, db, alice, advisor, monkeypatch
):
    from labs.m8_advisor_assistant import (
        answer_client_question as m8_answer_module,
    )

    def unfinished_m8(*args, **kwargs):
        raise NotImplementedError("M8 is not complete")

    monkeypatch.setattr(
        m8_answer_module, "answer_client_question", unfinished_m8
    )
    response = client.post(
        f"/advisor/clients/{alice.id}/assistant",
        params={"advisor_user_id": advisor.id},
        json={"question": "How is this portfolio positioned?"},
    )
    assert response.status_code == 200
    assert response.json()["route"] == "portfolio"


def test_decision_endpoint_round_trip(client, db, alice, advisor,
                                      canned_assistant):
    draft_id = client.post(
        f"/advisor/clients/{alice.id}/assistant",
        params={"advisor_user_id": advisor.id},
        json={"question": "How is this portfolio positioned?"},
    ).json()["draft_id"]
    decided = client.post(
        f"/advisor/drafts/{draft_id}/decision",
        params={"advisor_user_id": advisor.id},
        json={"decision": APPROVED_STATUS, "reason": "checked"},
    )
    assert decided.status_code == 200
    assert decided.json()["status"] == APPROVED_STATUS
    queue = client.get(
        "/advisor/drafts", params={"advisor_user_id": advisor.id}
    ).json()
    assert queue == []


def test_client_messages_appear_only_after_approval(client, db, alice,
                                                    advisor,
                                                    canned_assistant):
    draft_id = client.post(
        f"/advisor/clients/{alice.id}/assistant",
        params={"advisor_user_id": advisor.id},
        json={"question": "How is this portfolio positioned?"},
    ).json()["draft_id"]
    before = client.get("/messages", params={"user_id": alice.id}).json()
    assert before == []
    client.post(
        f"/advisor/drafts/{draft_id}/decision",
        params={"advisor_user_id": advisor.id},
        json={"decision": APPROVED_STATUS, "reason": "checked"},
    )
    after = client.get("/messages", params={"user_id": alice.id}).json()
    assert [message["draft_id"] for message in after] == [draft_id]


# -- step 3: memory ----------------------------------------------------


FOLLOW_UP = "Why is that a problem for Alice?"
POLICY_OPENER = "What does the concentration guideline say?"


def test_followup_keeps_the_thread_with_history(db, alice,
                                                canned_assistant):
    alone = answer_with_memory(db, alice.id, FOLLOW_UP, None)
    with_history = answer_with_memory(
        db, alice.id, FOLLOW_UP, [POLICY_OPENER]
    )
    assert alone.route == "portfolio"  # the thread is lost
    assert with_history.route == "policy"  # the thread is kept


def test_trade_words_in_a_followup_still_refuse(db, alice,
                                                canned_assistant):
    answer = answer_with_memory(
        db, alice.id, "Should we sell some of it?", [POLICY_OPENER]
    )
    assert answer.refused is True
    assert answer.route == "trade"


def test_long_history_is_windowed_before_routing(db, alice,
                                                 canned_assistant,
                                                 monkeypatch):
    seen = {}

    def spying_condense(history, *args, **kwargs):
        seen["history"] = list(history)
        return condense_conversation_history(history, *args, **kwargs)

    monkeypatch.setattr(
        memory_module, "condense_conversation_history", spying_condense
    )
    long_history = [f"How is holding number {i} doing?" for i in range(10)]
    answer = answer_with_memory(db, alice.id, FOLLOW_UP, long_history)
    assert seen["history"] == long_history
    assert answer.route == "portfolio"


# -- stretch: the model judge (skipped until implemented) --------------


def _fake_generator(reply: str):
    def generator(messages, max_new_tokens=10):
        return [
            {
                "generated_text": [
                    *messages, {"role": "assistant", "content": reply}
                ]
            }
        ]

    return generator


def test_judge_skips_when_no_model():
    try:
        result = judge_note_with_model("a note", "within guidelines")
    except NotImplementedError:
        pytest.skip("stretch: judge_note_with_model not implemented")
    assert result is None


def test_judge_parses_model_replies_defensively(monkeypatch):
    monkeypatch.setattr(
        judge_module,
        "load_offline_language_model",
        lambda: _fake_generator("Yes, the note states the verdict."),
    )
    try:
        confident = judge_note_with_model("a note", "within guidelines")
    except NotImplementedError:
        pytest.skip("stretch: judge_note_with_model not implemented")
    assert confident == "YES"

    monkeypatch.setattr(
        judge_module,
        "load_offline_language_model",
        lambda: _fake_generator(
            "As a language model, I cannot be certain about this."
        ),
    )
    hedged = judge_note_with_model("a note", "within guidelines")
    assert hedged == "NO"
