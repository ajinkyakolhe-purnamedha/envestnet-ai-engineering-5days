"""One concept: smolagents runs a real local-model tool-calling loop."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from smolagents import ToolCallingAgent, tool

from local_hf_agent import LiveSmolAgentsModel
from workshop_framework_setup import check_guideline, get_current_price


@tool
def price_tool(symbol: str) -> dict:
    """Return the simulated current price for one ticker.

    Args:
        symbol: Ticker symbol, for example AAPL.
    """

    return get_current_price(symbol)


@tool
def guideline_tool(symbol: str, proposed_allocation_pct: float) -> dict:
    """Check whether a proposed allocation exceeds the 35% limit.

    Args:
        symbol: Ticker symbol, for example AAPL.
        proposed_allocation_pct: Proposed allocation percent.
    """

    return check_guideline(symbol, proposed_allocation_pct)


model = LiveSmolAgentsModel()
agent = ToolCallingAgent(tools=[price_tool, guideline_tool], model=model, max_steps=4)
agent_error = None
try:
    agent_result = agent.run("Can Alice raise AAPL to 36% of the portfolio?", max_steps=4)
except Exception as error:
    agent_result = None
    agent_error = f"{type(error).__name__}: {error}"

agent_summary = {
    "framework": "smolagents",
    "agent_class": agent.__class__.__name__,
    "tools": ["get_current_price", "check_guideline"],
    "loop_limit": "max_steps",
    "model_calls": model.call_count,
}
runtime = {
    "backend": "local Hugging Face inference",
    "model": model.model_id,
    "model_calls": model.call_count,
    "latency_ms": model.last_generation_latency_ms,
}

print("Runtime:", runtime)
print("Raw model text:", model.last_response)
print("smolagents agent shape:", agent_summary)
if agent_error:
    print("Agent stopped after live model output:", agent_error)
print("Agent result:", agent_result)
