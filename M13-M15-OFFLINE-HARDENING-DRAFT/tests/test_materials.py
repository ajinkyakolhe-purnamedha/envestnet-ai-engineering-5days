"""Focused contracts for the isolated M13–M15 draft materials."""

import sys
from pathlib import Path

draft_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(draft_root / "m14_harness_redteaming"))
from harness_runtime import evaluate_request


def test_every_module_has_live_code_readme_and_dense_outline():
    modules = {
        "m13_testing_evaluating": "00_live_local_golden_eval.py",
        "m14_harness_redteaming": "00_live_weak_path.py",
        "m15_observability_deployment": "00_trace_live_run.py",
    }
    for module, live_card in modules.items():
        assert (draft_root / module / live_card).is_file()
        assert (draft_root / module / "README.md").is_file()
    assert len(list((draft_root / "slides").glob("*.md"))) == 3


def test_harness_denies_before_returning_data_and_bounds_repetition():
    denied = evaluate_request({"tool": "export_all_holdings", "client_id": "alice", "max_positions": 1}, "advisor_01")
    contained = evaluate_request({"tool": "get_portfolio_summary", "client_id": "alice", "max_positions": 1}, "advisor_01", step_count=3)
    assert denied["status"] == "blocked" and denied["result"] is None
    assert contained["status"] == "contained" and contained["reason"] == "step_limit_reached"


def test_outlines_keep_the_two_hour_sequence_and_correct_security_boundary():
    outline_text = "\n".join(path.read_text() for path in (draft_root / "slides").glob("*.md"))
    assert outline_text.count("40-minute") == 3
    assert "application-level containment" in outline_text
    assert "not filesystem/process/network isolation" in outline_text
    assert "test → harden → observe/deploy" in outline_text
