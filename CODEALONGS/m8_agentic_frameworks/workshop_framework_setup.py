"""Shared deterministic tools for M8 framework snippets."""

from __future__ import annotations

import sys
from pathlib import Path

M7_DIR = Path(__file__).resolve().parents[1] / "m7_agentic_applications"
sys.path.insert(0, str(M7_DIR))

from workshop_agentic_setup import (  # noqa: E402
    QUESTION,
    check_guideline,
    get_current_price,
    get_portfolio_allocation,
    summarize_guideline,
)


def draft_advisor_note(price: dict, allocation: dict, guideline: dict) -> dict:
    """Create a deterministic advisor note from tool observations."""

    answer = summarize_guideline(guideline)
    answer["evidence"] = [
        f"{price['symbol']} price is {price['price']}",
        f"{allocation['client']} currently holds {allocation['allocation_pct']}% {allocation['symbol']}",
        f"Policy limit is {guideline['limit_pct']}%",
    ]
    return answer
