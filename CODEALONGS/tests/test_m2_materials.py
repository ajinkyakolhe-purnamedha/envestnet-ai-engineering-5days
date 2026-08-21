"""M2 teaches LLM-call behavior, multi-turn context, measurement, and embeddings."""

from pathlib import Path
from runpy import run_path
import sys


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "day_1" / "m2_model_tokens_context"
DECK = ROOT.parent / "SLIDES-markdown" / "m2-model-tokens-context.md"


SNIPPETS = [
    "01_single_turn_call.py",
    "02_multiturn_history_resend.py",
    "03_context_changes_answer.py",
    "04_count_multiturn_tokens.py",
    "05_cost_same_conversation.py",
    "06_text_to_token_ids.py",
    "07_vectors_for_meaning_search.py",
]


def run_snippet(snippet_name: str) -> dict[str, object]:
    sys.path.insert(0, str(MATERIALS))
    try:
        return run_path(MATERIALS / snippet_name)
    finally:
        sys.path.remove(str(MATERIALS))


def test_m2_has_seven_ordered_concept_snippets() -> None:
    numbered_files = sorted(path.name for path in MATERIALS.glob("[0-9][0-9]_*.py"))
    assert numbered_files == SNIPPETS

    for snippet_name in SNIPPETS:
        source = (MATERIALS / snippet_name).read_text()
        assert "Try:" in source
        assert "One concept:" in source


def test_m2_behavior_snippets_call_local_smolm() -> None:
    for snippet_name in (
        "01_single_turn_call.py",
        "02_multiturn_history_resend.py",
        "03_context_changes_answer.py",
    ):
        source = (MATERIALS / snippet_name).read_text()
        assert "from m2_smolm_setup import call_smolm" in source


def test_m2_smolm_helper_is_small() -> None:
    source = (MATERIALS / "m2_smolm_setup.py").read_text()
    assert len(source.splitlines()) <= 35
    assert "def call_smolm" in source
    assert "warnings" not in source


def test_m2_numbered_snippets_are_readable_teaching_scripts() -> None:
    forbidden_setup = ("sys.path.insert", "Path(__file__)", "os.chdir")

    for snippet_name in SNIPPETS:
        source = (MATERIALS / snippet_name).read_text()
        code_lines = [
            line
            for line in source.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

        assert len(code_lines) <= 45, snippet_name
        for forbidden in forbidden_setup:
            assert forbidden not in source, snippet_name


def test_single_turn_call_sends_instruction_context_and_prompt_to_model() -> None:
    module = run_snippet("01_single_turn_call.py")

    assert module["messages"] == [
        {"role": "system", "content": "Answer only from the supplied context."},
        {"role": "system", "content": "Context:\nPolicy: no holding may exceed 35%."},
        {"role": "user", "content": "Is AAPL too large at 42%?"},
    ]
    assert module["reply"]
    assert "42%" in module["messages"][-1]["content"]


def test_second_turn_resends_history_and_changes_answer() -> None:
    module = run_snippet("02_multiturn_history_resend.py")

    assert [message["role"] for message in module["turn_two_messages"][1:]] == ["user", "assistant", "user"]
    assert module["turn_two_messages"][1]["content"] == "What do I hold?"
    assert module["turn_two_messages"][-1]["content"] == "Is that too much?"
    assert module["turn_one_reply"]
    assert module["turn_two_reply"]
    assert "AAPL" in module["turn_two_messages"][2]["content"]


def test_context_changes_answer_for_the_same_question() -> None:
    module = run_snippet("03_context_changes_answer.py")

    assert module["strict_reply"]
    assert module["permissive_reply"]
    assert "35%" in module["strict_context"]
    assert "50%" in module["permissive_context"]


def test_cost_same_conversation_uses_the_same_token_budget_for_every_model() -> None:
    module = run_path(MATERIALS / "05_cost_same_conversation.py")

    assert module["input_tokens"] > 0
    assert module["expected_output_tokens"] == 120
    assert module["small_cost"] < module["medium_cost"] < module["large_cost"]


def test_text_to_token_ids_keeps_tokens_separate_from_embeddings() -> None:
    module = run_path(MATERIALS / "06_text_to_token_ids.py")

    assert module["text"] == "AAPL concentration risk"
    assert len(module["token_ids"]) == len(module["tokens"])
    assert "embedding" not in module["__doc__"].lower()


def test_m2_deck_and_lab_use_the_new_courseware() -> None:
    deck = DECK.read_text()
    assert "CODEALONGS/day_1/m1_model_access/" in deck
    for snippet_name in SNIPPETS:
        assert f"CODEALONGS/day_1/m2_model_tokens_context/{snippet_name}" in deck
    assert "_code_along.py" not in deck
    assert "litellm" in deck
    assert "tokencost" in deck
    assert "Cost / latency / model size" in deck
    for name in ("README.md", "mini_lab.py", "starter.py", "hints.md", "solution.py"):
        assert (MATERIALS / "lab" / name).exists()
