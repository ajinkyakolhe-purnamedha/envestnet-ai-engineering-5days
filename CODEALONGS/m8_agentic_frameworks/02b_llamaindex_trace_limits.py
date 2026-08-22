"""One concept: framework step limits are the same safety idea as max_turns.

LlamaIndex alternative to 02_smolagents_trace_limits.py — but here the
framework really runs: a bad planner keeps requesting a tool that does not
exist, the trace records every failed observation, and `max_iterations`
stops the loop with a controlled failure instead of spinning forever.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core.agent.workflow import ReActAgent, ToolCallResult
from llama_index.core.llms import CompletionResponse, CustomLLM, LLMMetadata
from llama_index.core.tools import FunctionTool

from workshop_framework_setup import get_current_price

# #region bad_planner
BAD_STEP = (
    "Thought: call the price tool.\n"
    'Action: price_lookup\nAction Input: {"symbol": "AAPL"}'
)


class BadPlanner(CustomLLM):
    """Always requests a tool that is not registered."""

    calls: int = 0

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(model_name="bad-planner")

    def complete(self, prompt: str, formatted: bool = False, **kwargs) -> CompletionResponse:
        self.calls += 1
        return CompletionResponse(text=BAD_STEP)

    def stream_complete(self, prompt: str, formatted: bool = False, **kwargs):
        yield self.complete(prompt, formatted=formatted, **kwargs)
# #endregion bad_planner

# #region trace_limit
agent = ReActAgent(
    tools=[FunctionTool.from_defaults(fn=get_current_price)],
    llm=BadPlanner(),
)


async def run_until_blocked() -> tuple[list[dict], dict]:
    handler = agent.run("What is the AAPL price?", max_iterations=3)
    trace = []
    async for event in handler.stream_events():
        if isinstance(event, ToolCallResult):
            trace.append(
                {"step": len(trace) + 1, "observation": str(event.tool_output)}
            )
    try:
        await handler
        blocked = {}
    except Exception as exc:
        blocked = {
            "reason": "max_iterations",
            "error": type(exc).__name__,
            "message": "Stop the agent and return a controlled failure "
            "instead of looping forever.",
        }
    return trace, blocked


trace, blocked = asyncio.run(run_until_blocked())
# #endregion trace_limit

print("Trace:")
for item in trace:
    print(item)
print("Blocked:", blocked)
