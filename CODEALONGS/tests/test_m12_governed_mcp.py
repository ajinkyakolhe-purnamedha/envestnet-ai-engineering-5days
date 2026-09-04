"""Behaviour checks for the small M12 teaching snippets."""

from pathlib import Path
import json
import re
import subprocess
import sys


M12 = Path(__file__).resolve().parents[1] / "m12_governed_mcp"
ROOT = M12.parents[1]


def run_card(name: str) -> str:
    result = subprocess.run(
        [sys.executable, str(M12 / name)], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


def test_overview_card_shows_the_whole_permit_or_deny_path():
    output = run_card("00_governed_request.py")

    assert "ALLOW alice: bounded Chronos facts" in output
    assert "DENY bob: unassigned_client; no data read" in output
    assert "Next: make this same path real over MCP in 04/05." in output


def test_admission_card_shows_discovery_is_not_authority():
    output = run_card("01_admit_tools.py")

    assert "Model-visible: ['advisor_client_review']" in output
    assert "Excluded: ['export_all_holdings']" in output


def test_authorization_card_denies_before_it_reads_data():
    output = run_card("02_authorize_before_read.py")

    assert "ALLOW alice: read service called" in output
    assert "DENY bob: unassigned_client; read service not called" in output


def test_bound_result_card_makes_the_limit_visible():
    output = run_card("03_bound_result.py")

    assert "Returned positions: 2 of 3" in output
    assert "Truncated for model context: True" in output
    assert "DENY: max_positions must be 1 or 2" in output


def test_live_mcp_card_discovers_then_proves_permit_and_denial():
    output = run_card("05_permit_deny_prove.py")

    assert "Discovered: ['advisor_client_review']" in output
    assert "ALLOW:" in output
    assert "DENY:" in output
    assert "downstream_executed" in output
    assert "correlation_id" in output


def test_approval_card_keeps_a_client_note_internal():
    output = run_card("06_approval_required.py")

    assert "status: approval_required" in output
    assert "client_delivery_executed: False" in output
    assert "portfolio_mutation_executed: False" in output


def test_complete_walkthrough_combines_review_audit_and_approval():
    output = run_card("08_complete_walkthrough.py")

    assert "Discovered: ['advisor_client_review', 'prepare_client_note']" in output
    assert "ALLOW:" in output
    assert "DENY:" in output
    assert "APPROVAL:" in output
    assert "correlation_id" in output


def test_m12_deck_and_lab_point_to_the_governed_mcp_learning_path():
    """Keeps the delivered slides, lab, and runnable M12 snippets aligned."""
    deck = (ROOT / "SLIDES-markdown" / "m12-mcp-security-governance.md").read_text()
    lab = (ROOT / "SLIDES-markdown" / "m12-lab-instructions.md").read_text()

    for source in [
        "00_governed_request.py",
        "01_admit_tools.py",
        "02_authorize_before_read.py",
        "03_bound_result.py",
        "05_permit_deny_prove.py",
        "06_approval_required.py",
        "08_complete_walkthrough.py",
    ]:
        assert source in deck

    assert "60 minutes" in lab
    assert "starter_server.py" in lab
    assert "progress_check.py" in lab
    timings = [int(value) for value in re.findall(r"Timing: (\d+) minute", deck)]
    assert sum(timings) == 60
    assert (M12 / "lab" / "starter_server.py").exists()
    assert (M12 / "lab" / "client.py").exists()
    assert (M12 / "lab" / "progress_check.py").exists()


def test_lab_client_runs_a_real_mcp_exchange_with_parseable_scenarios():
    """The starter must be an observable MCP exchange, even before completion."""
    output = run_card("lab/client.py")

    assert 'DISCOVERED: ["advisor_client_review"]' in output
    for label in ["ALICE", "BOB", "OVER_LIMIT"]:
        line = next(line for line in output.splitlines() if line.startswith(f"{label}:"))
        assert json.loads(line.split(":", 1)[1])["status"] == "not_ready"
