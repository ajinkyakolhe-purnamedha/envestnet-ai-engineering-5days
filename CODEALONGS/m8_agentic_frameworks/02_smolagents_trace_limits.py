"""One concept: a live local model can fail inside a framework step limit."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from smolagents import ToolCallingAgent, tool

from local_hf_agent import LiveSmolAgentsModel
from workshop_framework_setup import get_current_price


@tool
def price_tool(symbol: str) -> dict:
    """Return the simulated current price for one ticker.

    Args:
        symbol: Ticker symbol, for example AAPL.
    """

    return get_current_price(symbol)


model = LiveSmolAgentsModel(max_new_tokens=64)
agent = ToolCallingAgent(tools=[price_tool], model=model, max_steps=3)
agent_error = None
try:
    agent_result = agent.run("Use price_tool to find the current AAPL price.", max_steps=3)
except Exception as error:
    agent_result = None
    agent_error = f"{type(error).__name__}: {error}"

trace = [{"step": model.call_count, "model_output": model.last_response}]
blocked = {
    "reason": "framework_stop" if agent_error else "completed",
    "message": agent_error or "The framework accepted the live model response.",
}
runtime = {
    "backend": "local Hugging Face inference",
    "model": model.model_id,
    "model_calls": model.call_count,
    "latency_ms": model.last_generation_latency_ms,
    "max_steps": 3,
}

print("Runtime:", runtime)
print("Trace:")
for item in trace:
    print(item)
print("Blocked:", blocked)
print("Agent result:", agent_result)
