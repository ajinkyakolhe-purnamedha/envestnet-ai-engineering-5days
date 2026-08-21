"""One concept: many agentic apps are controlled workflows plus tool calls."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from workshop_framework_setup import check_guideline, draft_advisor_note, get_current_price, get_portfolio_allocation


def route(question: str) -> str:
    return "portfolio_guideline" if "AAPL" in question and "36%" in question else "general"


def gather_parallel_inputs() -> tuple[dict, dict]:
    price = get_current_price("AAPL")
    allocation = get_portfolio_allocation("Alice", "AAPL")
    return price, allocation


def evaluate(note: dict) -> dict:
    note["review"] = "approved_for_demo" if "35%" in note["note"] else "needs_revision"
    return note


route_name = route("Can Alice raise AAPL to 36%?")
price_result, allocation_result = gather_parallel_inputs()
guideline_result = check_guideline("AAPL", 36.0)
workflow_output = evaluate(draft_advisor_note(price_result, allocation_result, guideline_result))

print("Route:", route_name)
print("Workflow output:", workflow_output)
