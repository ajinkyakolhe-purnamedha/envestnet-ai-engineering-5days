"""Behavior tests for the M11 governed-data code-along."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


M11 = Path(__file__).resolve().parents[1] / "m11_enterprise_data_tools"


def load_data_product():
    spec = importlib.util.spec_from_file_location(
        "m11_governed_data_product", M11 / "governed_data_product.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_portfolio_snapshot_is_bounded_and_includes_provenance():
    """Catches a change that exposes every holding or omits data origin."""
    data_product = load_data_product()

    result = data_product.build_current_portfolio_snapshot("alice", max_positions=2)

    assert result["client_id"] == "alice"
    assert len(result["holdings"]) == 2
    assert result["source"] == "mini_chronos_portfolio_service"
    assert result["simulated_date"] == "2026-08-29"


def test_portfolio_snapshot_rejects_requests_above_its_result_limit():
    """Catches removal of the data product's fixed result bound."""
    data_product = load_data_product()

    with pytest.raises(ValueError, match="max_positions must be between 1 and 3"):
        data_product.build_current_portfolio_snapshot("alice", max_positions=4)


def test_advisor_report_returns_deterministic_concentration_metrics():
    """Catches an advisor-review path that skips the deterministic analysis."""
    data_product = load_data_product()

    result = data_product.generate_advisor_review_report("alice")

    assert result["status"] == "ok"
    assert result["metrics"]["largest_position_symbol"] == "SPY"
    assert result["metrics"]["largest_position_percentage"] == 36.4
    assert result["source"] == "mini_chronos_advisor_service"


def test_investor_and_advisor_prompts_contain_their_governed_mcp_facts():
    """Catches a role flow that calls a model without its trusted facts."""
    spec = importlib.util.spec_from_file_location(
        "m11_model_explanation", M11 / "03_explain_live_governed_facts.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    investor = module.investor_messages(
        '{"source": "mini_chronos_portfolio_service"}'
    )
    advisor = module.advisor_messages(
        '{"source": "mini_chronos_advisor_service", "metrics": {}}'
    )

    assert "mini_chronos_portfolio_service" in investor[1]["content"]
    assert "Do not recommend trades" in investor[0]["content"]
    assert "mini_chronos_advisor_service" in advisor[1]["content"]
    assert "internal review draft" in advisor[0]["content"]
