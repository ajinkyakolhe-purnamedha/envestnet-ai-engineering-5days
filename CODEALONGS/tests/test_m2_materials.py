"""M2 keeps the M1 assistant progression inspectable and deterministic."""

from pathlib import Path
from runpy import run_path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "day_1" / "m2_model_tokens_context"
DECK = ROOT.parent / "SLIDES-markdown" / "m2-model-tokens-context.md"


def test_m2_has_six_paired_snippets_and_code_alongs() -> None:
    pairs = [
        ("01_messages_grow.py", "02_messages_grow_code_along.ipynb"),
        ("03_token_ids.py", "04_token_ids_code_along.ipynb"),
        ("05_count_context.py", "06_count_context_code_along.ipynb"),
        ("07_trim_history.py", "08_trim_history_code_along.ipynb"),
        ("09_embedding_similarity.py", "10_embedding_similarity_code_along.ipynb"),
        ("11_instrument_reply.py", "12_instrument_reply_code_along.ipynb"),
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


def test_trim_history_starts_with_a_user_message() -> None:
    trim_history = run_path(MATERIALS / "07_trim_history.py")["trim_history"]
    messages = [
        {"role": "user", "content": "First"},
        {"role": "assistant", "content": "One"},
        {"role": "user", "content": "Second"},
        {"role": "assistant", "content": "Two"},
        {"role": "user", "content": "Third"},
    ]

    retained = trim_history(messages, keep_turns=2)

    assert retained[0]["role"] == "user"
    assert retained == messages[2:]


def test_estimate_cost_uses_input_and_output_rates() -> None:
    estimate_cost = run_path(MATERIALS / "11_instrument_reply.py")["estimate_cost"]

    assert estimate_cost(1_000, 500, 0.002, 0.004) == 0.004


def test_m2_deck_and_lab_use_the_new_courseware() -> None:
    deck = DECK.read_text()
    assert "CODEALONGS/day_1/m1_model_access/" in deck
    assert "CODEALONGS/day_1/m2_model_tokens_context/01_messages_grow.py" in deck
    assert "routing" not in deck.lower()
    for name in ("README.md", "mini_lab.py", "starter.py", "hints.md", "solution.py"):
        assert (MATERIALS / "lab" / name).exists()
