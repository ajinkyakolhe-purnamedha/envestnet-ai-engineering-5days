"""Integrity checks for M1's snippet-to-code-along teaching contract."""

from pathlib import Path
from runpy import run_path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "m1_model_access"
DECK = ROOT.parent / "SLIDES-markdown" / "m1-intro-to-ai-models.md"


def test_m1_has_paired_snippets_and_code_alongs() -> None:
    pairs = [
        ("01_closed_model_call.py", "02_closed_model_call_code_along.ipynb"),
        ("03_local_model_call.py", "04_local_model_call_code_along.ipynb"),
        ("05_advisor_assistant.py", "06_advisor_assistant_code_along.ipynb"),
        ("07_cloud_hosted_models.py", "08_cloud_hosted_models_code_along.ipynb"),
    ]
    for snippet_name, notebook_name in pairs:
        snippet = MATERIALS / snippet_name
        notebook = MATERIALS / notebook_name
        assert snippet.exists()
        assert notebook.exists()
        first_code = next(
            cell["source"] for cell in nbformat.read(notebook, as_version=4)["cells"]
            if cell["cell_type"] == "code"
        )
        assert f'run_path("{snippet_name}")' in first_code


def test_m1_deck_uses_new_courseware_and_correct_cloud_boundary() -> None:
    deck = DECK.read_text()
    for snippet_name in (
        "01_closed_model_call.py",
        "03_local_model_call.py",
        "05_advisor_assistant.py",
        "07_cloud_hosted_models.py",
    ):
        assert f"CODEALONGS/m1_model_access/{snippet_name}" in deck
    assert "Gemini through Vertex AI" in deck
    assert "Bedrock is a separate cloud catalogue" in deck
    assert "open weights" in deck.lower()


def test_m1_snippets_are_direct_teaching_cards() -> None:
    limits = {
        "01_closed_model_call.py": 55,
        "03_local_model_call.py": 32,
        "05_advisor_assistant.py": 48,
        "07_cloud_hosted_models.py": 42,
    }
    for snippet_name, max_lines in limits.items():
        source = (MATERIALS / snippet_name).read_text()
        teaching_lines = [
            line for line in source.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        assert len(teaching_lines) <= max_lines

    advisor_source = (MATERIALS / "05_advisor_assistant.py").read_text()
    assert "hosted_backend" not in advisor_source
    assert "local_backend" not in advisor_source
    assert "call_smolm" in advisor_source


def test_m1_smolm_helper_is_small() -> None:
    source = (MATERIALS / "m1_smolm_setup.py").read_text()
    assert len(source.splitlines()) <= 25
    assert "def call_smolm" in source


def test_m1_advisor_assistant_calls_local_smolm() -> None:
    module = run_path(MATERIALS / "05_advisor_assistant.py")
    assert module["reply"]
    assert "AAPL" in module["prompt"]


def test_m1_defers_the_cloud_boundary_until_after_the_lab() -> None:
    """The governed-cloud section is the epilogue, not a mid-module detour."""
    deck = DECK.read_text()
    lab = deck.index("M1.L \u00b7 Lab")
    assert deck.index("M1.2.2 \u00b7 Three proprietary SDKs") < lab
    assert deck.index("M1.5.1 \u00b7 Build the assistant") < lab
    assert lab < deck.index("M1.6.1 \u00b7 Cloud platforms")


def test_m1_covers_application_opportunity_and_has_a_lab_pack() -> None:
    deck = DECK.read_text()
    for heading in (
        "AI becomes useful where work already happens",
        "Model families and the capability landscape",
        "Find an AI application opportunity",
        "Cloud platforms provide a governed model boundary",
        "Proprietary and open-weight models are different trade-offs",
    ):
        assert heading in deck

    lab = MATERIALS / "lab"
    assert (lab / "README.md").exists()
    assert (lab / "mini_lab.py").exists()
    assert (lab / "starter.py").exists()
    assert (lab / "solution.py").exists()


def test_lab_solution_builds_history_and_handles_empty_model_output() -> None:
    reply = run_path(MATERIALS / "lab" / "solution.py")["reply"]

    messages_seen: list[list[dict[str, str]]] = []

    def empty_model(messages: list[dict[str, str]]) -> str:
        messages_seen.append(messages)
        return ""

    result = reply("What changed?", [{"role": "user", "content": "Earlier"}], empty_model)

    assert messages_seen[0][0]["role"] == "system"
    assert messages_seen[0][-1] == {"role": "user", "content": "What changed?"}
    assert result == "I could not produce an answer. Please try again."
