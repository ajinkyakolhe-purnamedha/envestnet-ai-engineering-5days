"""Same agent, PydanticAI. M7's contracts ARE the framework.

Needs GEMINI_API_KEY. Run:
    uv run --project ../CODE-ALONGS \
        python m8/pydanticai_agent.py
"""

from pydantic import BaseModel

from m8.advisor_tools import (QUESTION, check_guidelines,
                              get_current_price,
                              get_portfolio_allocation)


# #region agent
from pydantic_ai import Agent


class AdvisorNote(BaseModel):
    recommendation: str
    allowed: bool
    facts_checked: list[str]


agent = Agent(
    "google:gemini-2.5-flash-lite",
    tools=[get_current_price,
           get_portfolio_allocation,
           check_guidelines],
    output_type=AdvisorNote,
    system_prompt=("You are a Chronos Wealth advisor "
                   "assistant. Use the tools to check "
                   "facts before answering."),
)

result = agent.run_sync(QUESTION)
print(result.output)
# #endregion agent


for message in result.all_messages():
    print(type(message).__name__,
          [p.__class__.__name__ for p in message.parts])

# Observed run (gemini-2.5-flash-lite):
#   recommendation='Alice can not raise AAPL to 36% ...
#   allowed=False  facts_checked=[price, allocation,
#   guideline]  -- and the trace shows all THREE tools
#   called in one model response (parallel tool calls).
#
# M7's loop, validation, dispatch, and retry are gone --
# absorbed by Agent(...). What you wrote by hand is now
# configuration: the tools list is your registry, the
# type hints are your schemas, and AdvisorNote is a
# guaranteed-valid final answer. The framework even
# re-prompts the model when validation fails: your M7
# error-observation trick, built in.
