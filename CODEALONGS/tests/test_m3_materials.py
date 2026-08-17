"""M3 teaches pattern selection without implementing later modules early."""

from pathlib import Path
from runpy import run_path

import nbformat
import pytest


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "day_1" / "m3_application_patterns"
DECK = ROOT.parent / "SLIDES-markdown" / "m3-application-patterns.md"


def test_m3_has_five_paired_snippets_and_code_alongs() -> None:
    pairs = [
        ("01_assemble_prompt.py", "02_assemble_prompt_code_along.ipynb"),
        ("03_base_call.py", "04_base_call_code_along.ipynb"),
        ("05_prompted_extraction.py", "06_prompted_extraction_code_along.ipynb"),
        ("07_choose_pattern.py", "08_choose_pattern_code_along.ipynb"),
        ("09_test_contract.py", "10_test_contract_code_along.ipynb"),
    ]
    for snippet_name, notebook_name in pairs:
        assert (MATERIALS / snippet_name).exists()
        notebook = MATERIALS / notebook_name
        assert notebook.exists()
        first_code = next(
            cell["source"] for cell in nbformat.read(notebook, as_version=4)["cells"]
            if cell["cell_type"] == "code"
        )
        assert f'run_path("{snippet_name}")' in first_code


def test_assembled_prompt_keeps_its_three_parts_distinguishable() -> None:
    assemble_prompt = run_path(MATERIALS / "01_assemble_prompt.py")["assemble_prompt"]
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
    choose_pattern = run_path(MATERIALS / "07_choose_pattern.py")["choose_pattern"]
    assert choose_pattern(requirements) == expected


def test_trade_contract_rejects_an_allocation_above_the_policy_cap() -> None:
    validate_trade_request = run_path(MATERIALS / "09_test_contract.py")["validate_trade_request"]
    assert not validate_trade_request({"symbol": "AAPL", "allocation_percent": 36})
    assert validate_trade_request({"symbol": "AAPL", "allocation_percent": 35})


def test_prompted_extraction_uses_instructor_with_a_pydantic_response_model() -> None:
    source = (MATERIALS / "05_prompted_extraction.py").read_text()
    assert "import instructor" in source
    assert "response_model=TradeIntent" in source


def test_m3_deck_and_lab_use_new_courseware_and_five_patterns() -> None:
    deck = DECK.read_text()
    for pattern in ("Direct call", "Prompted application", "RAG", "Fine-tuning", "Agentic workflow"):
        assert pattern in deck
    assert "CODEALONGS/day_1/m3_application_patterns/01_assemble_prompt.py" in deck
    assert "SLIDES-markdown/m3/" not in deck
    for name in ("README.md", "mini_lab.md", "starter.md", "hints.md", "instructor_solution.md", "decision_table.csv"):
        assert (MATERIALS / "lab" / name).exists()
