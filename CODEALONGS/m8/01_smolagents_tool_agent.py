"""One concept: smolagents runs the tool-calling loop for an agent."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from smolagents import Model, ToolCallingAgent, tool
from smolagents.models import ChatMessage, ChatMessageToolCall, ChatMessageToolCallFunction, MessageRole

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


def tool_call(name: str, args: dict, call_id: str) -> ChatMessageToolCall:
    function = ChatMessageToolCallFunction(name=name, arguments=args)
    return ChatMessageToolCall(id=call_id, type="function", function=function)


class ClassroomModel(Model):
    """Tiny local planner so the snippet teaches smolagents execution."""

    def __init__(self):
        super().__init__()
        self.calls = 0

    def generate(self, messages, tools_to_call_from=None, **kwargs) -> ChatMessage:
        self.calls += 1
        if self.calls == 1:
            call = tool_call("price_tool", {"symbol": "AAPL"}, "call-1")
        elif self.calls == 2:
            call = tool_call("guideline_tool", {"symbol": "AAPL", "proposed_allocation_pct": 36.0}, "call-2")
        else:
            call = tool_call("final_answer", {"answer": "Not allowed: 36% is above the 35% limit."}, "call-3")
        return ChatMessage(role=MessageRole.ASSISTANT, tool_calls=[call])


model = ClassroomModel()
agent = ToolCallingAgent(tools=[price_tool, guideline_tool], model=model, max_steps=4)
agent_result = agent.run("Can Alice raise AAPL to 36% of the portfolio?", max_steps=4)

agent_summary = {
    "framework": "smolagents",
    "agent_class": agent.__class__.__name__,
    "tools": ["get_current_price", "check_guideline"],
    "loop_limit": "max_steps",
    "model_calls": model.calls,
}

print("smolagents agent shape:", agent_summary)
print("Agent result:", agent_result)
