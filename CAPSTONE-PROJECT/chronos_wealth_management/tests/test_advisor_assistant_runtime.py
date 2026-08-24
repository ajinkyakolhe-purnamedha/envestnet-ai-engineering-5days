"""Route-facing advisor assistant runtime behavior."""

from chronos.advisor_assistant_runtime import (
    answer_advisor_question,
    decide_advisor_note_draft,
    judge_advisor_note,
    submit_advisor_note_for_approval,
)
from chronos.shared_database.domain_errors import NoteDraftAlreadyDecidedError


def test_runtime_answers_with_the_production_reference_when_no_history(db, alice):
    answer = answer_advisor_question(
        db, alice.id, "How is this portfolio positioned?"
    )

    assert answer.route == "portfolio"
    assert answer.refused is False
    assert answer.metrics is not None
    assert answer.note_source == "m9_reference"


def test_runtime_uses_history_without_depending_on_lab_modules(db, alice):
    answer = answer_advisor_question(
        db,
        alice.id,
        "Why is that a problem for Alice?",
        ["What does the concentration guideline say?"],
    )

    assert answer.route == "policy"
    assert answer.metrics is None


def test_runtime_submits_and_decides_a_draft(db, alice, advisor):
    answer = answer_advisor_question(
        db, alice.id, "How is this portfolio positioned?"
    )
    draft = submit_advisor_note_for_approval(
        db, advisor.id, alice.id, "How is this portfolio positioned?", answer
    )

    decided = decide_advisor_note_draft(
        db, advisor.id, draft.draft_id, "approved", "checked"
    )

    assert draft.status == "pending"
    assert decided.status == "approved"


def test_runtime_prevents_a_second_draft_decision(db, alice, advisor):
    answer = answer_advisor_question(
        db, alice.id, "How is this portfolio positioned?"
    )
    draft = submit_advisor_note_for_approval(
        db, advisor.id, alice.id, "How is this portfolio positioned?", answer
    )
    decide_advisor_note_draft(db, advisor.id, draft.draft_id, "rejected", "tone")

    try:
        decide_advisor_note_draft(db, advisor.id, draft.draft_id, "approved", "changed")
    except NoteDraftAlreadyDecidedError:
        return
    raise AssertionError("a decided draft must remain final")


def test_runtime_skips_an_unavailable_optional_judge():
    def unavailable_judge(note, verdict):
        raise NotImplementedError("optional runtime judge is disabled")

    assert judge_advisor_note("A note", "within guidelines", unavailable_judge) is None
