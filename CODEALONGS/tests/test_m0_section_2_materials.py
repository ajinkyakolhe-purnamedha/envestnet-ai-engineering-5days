"""Checks for the M0.2 package, local-model, and hosted-model materials."""

from pathlib import Path

import nbformat


MATERIALS = (
    Path(__file__).resolve().parents[1]
    / "day_1"
    / "m0_python_foundations"
    / "02_packages_and_model_access"
)


def test_section_two_has_one_artifact_per_teaching_move():
    assert (MATERIALS / "01_install_packages.sh").is_file()
    assert (MATERIALS / "02_huggingface_offline.py").is_file()
    assert (MATERIALS / "03_gemini_api.py").is_file()
    assert (MATERIALS / "04_huggingface_code_along.ipynb").is_file()
    assert (MATERIALS / "05_gemini_code_along.ipynb").is_file()


def test_install_card_uses_real_uv_package_commands():
    install_card = (MATERIALS / "01_install_packages.sh").read_text()

    assert "uv init wealth-demo" in install_card
    assert "uv add transformers torch" in install_card
    assert "uv add google-genai" in install_card
    assert "uv add python-dotenv" in install_card
    assert "uv add fastapi uvicorn" in install_card
    assert "uv add openai anthropic boto3" in install_card


def test_each_code_along_starts_with_its_matching_snippet():
    for number, notebook_name, snippet_name in [
        ("04", "huggingface", "02_huggingface_offline.py"),
        ("05", "gemini", "03_gemini_api.py"),
    ]:
        notebook = nbformat.read(
            MATERIALS / f"{number}_{notebook_name}_code_along.ipynb",
            as_version=4,
        )
        first_code_cell = next(
            cell for cell in notebook.cells if cell.cell_type == "code"
        )

        assert snippet_name in first_code_cell.source or first_code_cell.source == (
            MATERIALS / snippet_name
        ).read_text().rstrip()


def test_gemini_snippet_loads_the_key_from_dotenv():
    gemini_snippet = (MATERIALS / "03_gemini_api.py").read_text()

    assert "from dotenv import load_dotenv" in gemini_snippet
    assert "load_dotenv(override=True)" in gemini_snippet
    assert "COURSEWARE_OFFLINE" not in gemini_snippet
    assert "gemini-3.5-flash-lite" in gemini_snippet
