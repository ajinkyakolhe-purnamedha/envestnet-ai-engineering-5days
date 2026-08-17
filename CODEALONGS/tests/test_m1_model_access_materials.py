"""Integrity checks for M1's snippet-to-code-along teaching contract."""

from pathlib import Path
from runpy import run_path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "day_1" / "m1_model_access"
DECK = ROOT.parent / "SLIDES-markdown" / "m1-intro-to-ai-models.md"


def test_m1_has_paired_snippets_and_code_alongs() -> None:
    pairs = [
        ("01_gemini_text.py", "02_gemini_text_code_along.ipynb"),
        ("03_vertex_gemini.py", "04_vertex_gemini_code_along.ipynb"),
        ("05_hosted_open_model.py", "06_hosted_open_model_code_along.ipynb"),
        ("07_local_model.py", "08_local_model_code_along.ipynb"),
        ("09_model_boundary.py", "10_model_boundary_code_along.ipynb"),
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
        assert f"run_path(\"{snippet_name}\")" in first_code


def test_m1_deck_uses_new_courseware_and_correct_cloud_boundary() -> None:
    deck = DECK.read_text()
    assert "CODEALONGS/day_1/m1_model_access/01_gemini_text.py" in deck
    assert "Gemini through Vertex AI" in deck
    assert "Bedrock is a separate cloud catalogue" in deck
    assert "open weights" in deck.lower()


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
