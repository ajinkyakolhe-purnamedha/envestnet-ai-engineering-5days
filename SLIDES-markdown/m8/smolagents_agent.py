"""Same agent, smolagents -- fully offline on SmolLM2.

The participants' framework: no key, local weights only.
Run:
    uv run python -m m8.smolagents_agent
"""

from chronos_offline import CHAT_MODEL


# #region agent
from smolagents import ToolCallingAgent, TransformersModel, tool


@tool
def get_current_price(symbol: str) -> dict:
    """Latest close for one symbol on the simulated date.

    Args:
        symbol: Ticker symbol, for example AAPL.
    """
    prices = {"AAPL": 80.46, "MSFT": 182.83, "GLD": 163.66}
    return {"symbol": symbol, "close": prices[symbol]}


@tool
def check_guidelines(symbol: str,
                     proposed_allocation_pct: float) -> dict:
    """Is the proposed allocation within the 35% limit?

    Args:
        symbol: Ticker symbol, for example AAPL.
        proposed_allocation_pct: Proposed percent, 0-100.
    """
    return {"symbol": symbol, "limit_pct": 35.0,
            "allowed": proposed_allocation_pct <= 35.0}


agent = ToolCallingAgent(
    tools=[get_current_price, check_guidelines],
    model=TransformersModel(model_id=str(CHAT_MODEL),
                            max_new_tokens=200),
    max_steps=3,
)

answer = agent.run("Can Alice raise AAPL to 36%? "
                   "Check price and guideline.")
print("FINAL:", answer)
# #endregion agent

# smolagents is built by Hugging Face for exactly our
# situation: small, local, open models. TransformersModel
# loads our committed SmolLM2 weights; the agent loop,
# tool schemas, max_steps, and the printed trace are the
# M7 runtime, packaged.
#
# Observed run (SmolLM2-135M, CPU, ~28s):
#   Step 1-3: "Error while parsing tool call from model
#             output" -- contained, loop continues
#   Step 4:   max_steps reached, model forced to answer:
#   FINAL: "Alice can raise AAPL to 36% by ..."  <- WRONG
#
# That wrong answer is the lesson. The runtime was
# perfect: every bad output became an error observation,
# max_steps stopped the loop, nothing crashed. But a
# 135M planner cannot emit a tool call, so the agent
# never checked a single fact -- then answered anyway.
# Planner quality gates agent quality. Do NOT fix this
# by hiding the trace; fix it in the lab by keeping the
# deterministic planner in charge and letting the model
# only draft the final note.
