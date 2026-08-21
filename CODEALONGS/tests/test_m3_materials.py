"""M3 teaches pattern selection without implementing later modules early."""

from pathlib import Path
from runpy import run_path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "day_1" / "m3_application_patterns"
DECK = ROOT.parent / "SLIDES-markdown" / "m3-application-patterns.md"


SNIPPETS = [
    "01_assemble_prompt.py",
    "02_direct_llm_call.py",
    "03_prompted_extraction.py",
    "04_simple_rag_architecture.py",
    "05_choose_pattern.py",
    "06_test_contract.py",
]


def run_snippet(snippet_name: str) -> dict[str, object]:
    sys.path.insert(0, str(MATERIALS))
    try:
        return run_path(MATERIALS / snippet_name)
    finally:
        sys.path.remove(str(MATERIALS))


def test_m3_has_six_ordered_simple_snippets() -> None:
    numbered_files = sorted(path.name for path in MATERIALS.glob("[0-9][0-9]_*.py"))
    assert numbered_files == SNIPPETS

    for snippet_name in SNIPPETS:
        source = (MATERIALS / snippet_name).read_text()
        assert "One concept:" in source
        assert "Try:" in source


def test_m3_pattern_snippets_call_local_smolm() -> None:
    for snippet_name in (
        "02_direct_llm_call.py",
        "03_prompted_extraction.py",
        "04_simple_rag_architecture.py",
    ):
        source = (MATERIALS / snippet_name).read_text()
        assert "from m3_smolm_setup import call_smolm" in source


def test_m3_smolm_helper_is_small() -> None:
    source = (MATERIALS / "m3_smolm_setup.py").read_text()
    assert len(source.splitlines()) <= 35
    assert "def call_smolm" in source
    assert "warnings" not in source


def test_m3_numbered_snippets_are_readable_teaching_scripts() -> None:
    forbidden_setup = ("sys.path.insert", "Path(__file__)", "os.chdir")

    for snippet_name in SNIPPETS:
        source = (MATERIALS / snippet_name).read_text()
        code_lines = [
            line
            for line in source.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

        assert len(code_lines) <= 55, snippet_name
        for forbidden in forbidden_setup:
            assert forbidden not in source, snippet_name


def test_assembled_prompt_keeps_its_three_parts_distinguishable() -> None:
    assemble_prompt = run_snippet("01_assemble_prompt.py")["assemble_prompt"]
    prompt = assemble_prompt("Be concise.", "AAPL is 52%.", "What is the risk?")

    assert "INSTRUCTION: Be concise." in prompt
    assert "CONTEXT: AAPL is 52%." in prompt
    assert "QUESTION: What is the risk?" in prompt


@pytest.mark.parametrize(
    ("requirements", "expected"),
    [
        ({"general_language"}, "base"),
        ({"format"}, "prompted"),
        ({"private_facts"}, "rag"),
        ({"repeated_behavior"}, "fine_tune"),
        ({"dynamic_steps"}, "agentic"),
    ],
)
def test_choose_pattern_uses_the_first_needed_capability(
    requirements: set[str], expected: str
) -> None:
    choose_pattern = run_path(MATERIALS / "05_choose_pattern.py")["choose_pattern"]
    assert choose_pattern(requirements) == expected


def test_trade_contract_rejects_an_allocation_above_the_policy_cap() -> None:
    validate_trade_request = run_snippet("06_test_contract.py")["validate_trade_request"]
    assert not validate_trade_request({"symbol": "AAPL", "allocation_percent": 36})
    assert validate_trade_request({"symbol": "AAPL", "allocation_percent": 35})


def test_prompted_extraction_uses_instructor_with_a_pydantic_response_model() -> None:
    source = (MATERIALS / "03_prompted_extraction.py").read_text()
    assert len(source.splitlines()) <= 50
    assert "import instructor" in source
    assert "response_model=TradeIntent" in source
    assert "validate_trade_intent" in source


def test_direct_call_and_rag_snippets_show_application_patterns() -> None:
    direct = run_snippet("02_direct_llm_call.py")
    assert direct["messages"][0]["role"] == "system"
    assert "52%" in direct["messages"][-1]["content"]
    assert direct["raw_reply"]

    rag = run_snippet("04_simple_rag_architecture.py")
    assert rag["retrieved_context"]["source"] == "policy"
    assert "35%" in rag["prompt"]
    assert rag["raw_answer"]


def test_m3_deck_and_lab_use_new_courseware_and_five_patterns() -> None:
    deck = DECK.read_text()
    for pattern in ("Direct call", "Prompted application", "RAG", "Fine-tuning", "Agentic workflow"):
        assert pattern in deck
    for snippet_name in SNIPPETS:
        assert f"CODEALONGS/day_1/m3_application_patterns/{snippet_name}" in deck
    assert "_code_along" not in deck
    assert "SLIDES-markdown/m3/" not in deck
    for name in ("README.md", "mini_lab.md", "starter.md", "hints.md", "instructor_solution.md", "decision_table.csv"):
        assert (MATERIALS / "lab" / name).exists()
