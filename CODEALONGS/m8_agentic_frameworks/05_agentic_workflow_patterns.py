"""One concept: many agentic apps are controlled workflows plus tool calls."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from workshop_framework_setup import check_guideline, get_current_price, get_portfolio_allocation
from local_hf_agent import LocalSmolFunctionLLM


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
llm = LocalSmolFunctionLLM()
model_draft = llm.complete(
    "Write one short internal advisor note using only these facts. "
    f"Price: {price_result}. Allocation: {allocation_result}. Policy result: {guideline_result}."
).text
workflow_output = evaluate(
    {
        "allowed": guideline_result["allowed"],
        "note": model_draft,
        "evidence": [price_result, allocation_result, guideline_result],
    }
)
runtime = {
    "backend": "local Hugging Face inference",
    "model": llm.metadata.model_name,
    "model_calls": llm.generation_count,
    "latency_ms": llm.last_generation_latency_ms,
}

print("Runtime:", runtime)
print("Raw model text:", llm.last_response)
print("Route:", route_name)
print("Workflow output:", workflow_output)
