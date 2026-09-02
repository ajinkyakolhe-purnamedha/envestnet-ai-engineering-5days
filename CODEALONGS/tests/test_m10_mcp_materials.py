"""Behavior checks for the M10 real-reuse demonstration."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys


M10 = Path(__file__).resolve().parents[1] / "m10_mcp_fundamentals"


def load_real_reuse_card():
    spec = importlib.util.spec_from_file_location(
        "m10_real_reuse", M10 / "05_real_reuse_with_models.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_investor_and_advisor_prompts_use_the_same_live_facts_differently():
    """Catches an app path that drops MCP facts or blurs its output boundary."""
    card = load_real_reuse_card()
    portfolio = '{"client": "alice", "cash": 25000}'
    policy = '{"evidence": "No single asset may exceed 35%."}'

    investor = card.investor_messages(portfolio, policy)
    advisor = card.advisor_messages(portfolio, policy)

    assert portfolio in investor[1]["content"]
    assert policy in investor[1]["content"]
    assert portfolio in advisor[1]["content"]
    assert policy in advisor[1]["content"]
    assert "Do not recommend trades" in investor[0]["content"]
    assert "internal meeting draft" in advisor[0]["content"]


def test_minimal_client_calls_a_tool_and_reads_a_resource():
    """The first MCP card must make both primitives observable to learners."""
    completed = subprocess.run(
        [sys.executable, str(M10 / "simple_mcp_client.py")],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "2 + 3 = 5" in completed.stdout
    assert "Greeting: Hello, Ada! Welcome to MCP." in completed.stdout
