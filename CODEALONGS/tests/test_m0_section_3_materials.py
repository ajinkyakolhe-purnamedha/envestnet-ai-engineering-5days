"""Behavior checks for the M0.3 incremental wealth-demo courseware."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import runpy
import sqlite3
import sys

import nbformat
import pytest


MATERIALS = (
    Path(__file__).resolve().parents[1]
   
    / "m0_python_foundations"
    / "03_wealth_demo"
)
sys.path.insert(0, str(MATERIALS))


def run_snippet(name: str) -> str:
    output = StringIO()
    with redirect_stdout(output):
        runpy.run_path(str(MATERIALS / name))
    return output.getvalue().strip()


def test_section_three_snippets_teach_small_observable_examples():
    assert run_snippet("01_variables_and_hints.py") == "AAPL purchase cost: 805.0"
    assert run_snippet("03_functions.py") == "Purchase cost: 805.0"
    assert run_snippet("05_classes.py") == "AAPL market value: 825.0"
    assert run_snippet("07_database.py") == "AAPL close on 2020-06-01: 80.46"
    assert "Selected AAPL price dated 2020-06-01" in run_snippet(
        "11_logging_testing_debugging.py"
    )


@pytest.mark.parametrize(
    ("notebook_name", "snippet_name"),
    [
        ("02_variables_and_hints_code_along.ipynb", "01_variables_and_hints.py"),
        ("04_functions_code_along.ipynb", "03_functions.py"),
        ("06_classes_code_along.ipynb", "05_classes.py"),
        ("08_database_code_along.ipynb", "07_database.py"),
        ("10_server_code_along.ipynb", "09_server.py"),
        ("12_logging_testing_debugging_code_along.ipynb", "11_logging_testing_debugging.py"),
    ],
)
def test_each_code_along_starts_with_the_matching_snippet(
    notebook_name: str, snippet_name: str
):
    notebook = nbformat.read(MATERIALS / notebook_name, as_version=4)
    first_code_cell = next(cell for cell in notebook.cells if cell.cell_type == "code")

    assert first_code_cell.source == (MATERIALS / snippet_name).read_text().rstrip()


def test_calculations_reject_bad_inputs_and_return_correct_gain_loss():
    from wealth_demo.calculations import gain_loss, purchase_cost

    assert gain_loss(805.0, 850.0) == 45.0
    with pytest.raises(ValueError, match="positive"):
        purchase_cost(0, 80.50)


def test_portfolio_purchase_updates_cash_and_rejects_insufficient_cash():
    from wealth_demo.models import Holding, Portfolio

    holding = Holding("AAPL", 10, 80.50)
    portfolio = Portfolio(cash=1_000.0)
    portfolio.buy(holding)
    assert portfolio.cash == 195.0
    assert portfolio.holdings == [holding]

    with pytest.raises(ValueError, match="cash"):
        Portfolio(cash=100.0).buy(holding)


def test_storage_returns_last_price_on_or_before_requested_date_and_saved_holding():
    from wealth_demo.models import Holding
    from wealth_demo.storage import (
        create_database,
        get_price_as_of,
        load_holdings,
        save_holding,
        seed_prices,
    )

    connection = sqlite3.connect(":memory:")
    create_database(connection)
    seed_prices(connection)
    save_holding(connection, Holding("AAPL", 10, 80.50))

    assert get_price_as_of(connection, "AAPL", "2020-06-01") == 80.46
    assert load_holdings(connection) == [Holding("AAPL", 10, 80.50)]


def test_server_and_final_material_make_operational_practices_visible():
    from fastapi.testclient import TestClient
    from wealth_demo.server import app

    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
    portfolio = client.get("/portfolio").json()
    assert portfolio["holdings"] == [
        {"symbol": "AAPL", "shares": 10, "purchase_price": 80.5}
    ]

    final_source = (MATERIALS / "11_logging_testing_debugging.py").read_text()
    assert "logger.info" in final_source
    assert "unittest" in final_source
    assert "breakpoint()" in final_source
