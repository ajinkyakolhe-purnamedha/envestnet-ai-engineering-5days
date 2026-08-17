"""Checks for the M0.1.2 snippet and its guided code-along."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import runpy

import nbformat


MATERIALS = (
    Path(__file__).resolve().parents[1]
    / "day_1"
    / "m0_python_foundations"
    / "01_share_purchase"
)
SNIPPET = MATERIALS / "01_purchase_cost.py"
NOTEBOOK = MATERIALS / "02_purchase_cost_code_along.ipynb"


def test_snippet_teaches_one_share_purchase_calculation():
    output = StringIO()

    with redirect_stdout(output):
        runpy.run_path(str(SNIPPET))

    assert output.getvalue().splitlines() == [
        "Cost: 805.0",
        "Cash left: 99195.0",
    ]


def test_code_along_starts_with_the_exact_snippet():
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    first_code_cell = next(
        cell for cell in notebook.cells if cell.cell_type == "code"
    )

    assert first_code_cell.source == SNIPPET.read_text().rstrip()
