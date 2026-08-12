"""Pattern 6: handoff. An agent becomes another's tool.

Fully offline (and honestly shaky on SmolLM2). Run:
    uv run python -m m8.pattern_handoff
"""

from chronos_offline import CHAT_MODEL
from smolagents import ToolCallingAgent, TransformersModel, tool


@tool
def get_current_price(symbol: str) -> dict:
    """Latest close for one symbol.

    Args:
        symbol: Ticker symbol, for example AAPL.
    """
    prices = {"AAPL": 80.46, "MSFT": 182.83, "GLD": 163.66}
    return {"symbol": symbol, "close": prices[symbol]}


# #region pattern
model = TransformersModel(model_id=str(CHAT_MODEL),
                          max_new_tokens=150)

research_agent = ToolCallingAgent(
    tools=[get_current_price],
    model=model, max_steps=2,
    name="researcher",
    description="Gathers facts about holdings.")

manager = ToolCallingAgent(
    tools=[], model=model, max_steps=3,
    managed_agents=[research_agent])

print(manager.run("Ask the researcher for the AAPL "
                  "price, then report it."))
# #endregion pattern

# managed_agents registers a whole agent the way M7
# registered a function: name + description + contract.
# That is the entire multi-agent idea. On SmolLM2 every
# planner in the chain stumbles (same lesson as the
# single agent, compounded) -- which is the honest
# warning: multi-agent multiplies planner risk. Split
# agents only when toolsets or instructions genuinely
# differ, never for style points.
