"""M9 closes agentic application building with memory, verification, and gates."""

from pathlib import Path
from runpy import run_path
import sys


ROOT = Path(__file__).resolve().parents[1]
M9 = ROOT / "m9_memory_verification_hitl"
DECK = ROOT.parent / "SLIDES-markdown" / "m9-memory-verification-hitl.md"

SNIPPETS = [
    "01_memory_is_messages.py",
    "02_bounded_memory.py",
    "03_effective_question.py",
    "04_verify_generated_draft.py",
    "05_model_judge.py",
    "06_human_gate_and_state.py",
]


def run_snippet(snippet_name: str) -> dict[str, object]:
    sys.path.insert(0, str(M9))
    try:
        return run_path(M9 / snippet_name)
    finally:
        sys.path.remove(str(M9))


def test_m9_has_five_section_agentic_closure_story() -> None:
    deck = DECK.read_text()

    expected_sections = [
        "M9.1 · From Agentic Workflow To Product Feature",
        "M9.2 · LlamaIndex Memory For Follow-Ups",
        "M9.3 · Verification Ladder",
        "M9.4 · Human Gate, State, And Trace",
        "M9.5 · Agentic Chapter Closure",
    ]
    for section in expected_sections:
        assert section in deck

    assert "M7  the loop" in deck
    assert "M8  the workflow" in deck
    assert "M9  the finished feature" in deck
    assert "Tomorrow: its tools are still hardwired. **MCP.**" in deck


def test_m9_deck_references_ordered_runnable_snippets() -> None:
    deck = DECK.read_text()

    numbered_files = sorted(path.name for path in M9.glob("[0-9][0-9]_*.py"))
    assert numbered_files == SNIPPETS

    for snippet in SNIPPETS:
        assert f"CODEALONGS/m9_memory_verification_hitl/{snippet}" in deck
        assert (M9 / snippet).exists()

    readme = (M9 / "README.md").read_text()
    for snippet in SNIPPETS:
        assert snippet in readme


def test_m9_numbered_snippets_are_small_teaching_scripts() -> None:
    forbidden_setup = ("sys.path.insert", "Path(__file__)", "os.chdir", "input(")

    for snippet in SNIPPETS:
        source = (M9 / snippet).read_text()
        code_lines = [
            line
            for line in source.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

        assert "One concept:" in source
        assert "Try:" in source
        assert len(code_lines) <= 95, snippet
        for forbidden in forbidden_setup:
            assert forbidden not in source, snippet


def test_m9_offline_model_helper_is_small_and_focused() -> None:
    source = (M9 / "chronos_offline.py").read_text()
    code_lines = [
        line
        for line in source.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    assert len(code_lines) < 50
    assert "def load_chat" in source
    assert "def generate" in source
    assert "def count_tokens" in source
    assert "def classify" not in source
    assert "def embed" not in source


def test_m9_numbered_snippets_run_and_expose_key_outputs() -> None:
    for snippet in SNIPPETS:
        module = run_snippet(snippet)
        assert module["__doc__"]

    memory = run_snippet("01_memory_is_messages.py")
    assert memory["with_memory_messages"][-1].content == memory["new_question"]
    assert memory["with_memory_reply"]

    window = run_snippet("02_bounded_memory.py")
    assert len(window["windowed_history"]) < len(window["full_history"])
    assert window["windowed_reply"]

    effective = run_snippet("03_effective_question.py")
    assert effective["effective_question"].endswith(effective["new_question"])
    assert effective["route"] == "policy"
    assert effective["rewrite_reply"]

    rules = run_snippet("04_verify_generated_draft.py")
    assert rules["review"]["passed"] in {True, False}
    assert rules["draft"]

    judge = run_snippet("05_model_judge.py")
    assert judge["agreements"] <= len(judge["NOTES"])
    assert isinstance(judge["judge_results"][0]["judge"], bool)

    gate = run_snippet("06_human_gate_and_state.py")
    assert gate["published"] == [gate["loaded_drafts"][0]]
    assert gate["loaded_drafts"][1]["status"] == "rejected"
    assert gate["draft_text"]
