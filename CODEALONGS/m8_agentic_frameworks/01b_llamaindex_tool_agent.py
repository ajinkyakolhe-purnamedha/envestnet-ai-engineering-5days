"""One concept: LlamaIndex runs the tool-calling loop for an agent.

LlamaIndex alternative to 01_smolagents_tool_agent.py — same scripted
classroom planner idea, so the framework's loop runs offline and
deterministically.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.llms import CompletionResponse, CustomLLM, LLMMetadata
from llama_index.core.tools import FunctionTool

from workshop_framework_setup import check_guideline, get_current_price

# #region planner
PLANNER_SCRIPT = [
    "Thought: I need the current price first.\n"
    'Action: get_current_price\nAction Input: {"symbol": "AAPL"}',
    "Thought: Now check the guideline.\n"
    "Action: check_guideline\n"
    'Action Input: {"symbol": "AAPL", "proposed_allocation_pct": 36.0}',
    "Thought: I can answer now.\n"
    "Answer: Not allowed: 36% is above the 35% limit.",
]


class ClassroomPlanner(CustomLLM):
    """Tiny scripted planner so the snippet teaches LlamaIndex execution."""

    calls: int = 0

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(model_name="classroom-scripted-planner")

    def complete(self, prompt: str, formatted: bool = False, **kwargs) -> CompletionResponse:
        text = PLANNER_SCRIPT[min(self.calls, len(PLANNER_SCRIPT) - 1)]
        self.calls += 1
        return CompletionResponse(text=text)

    def stream_complete(self, prompt: str, formatted: bool = False, **kwargs):
        yield self.complete(prompt, formatted=formatted, **kwargs)
# #endregion planner

# #region agent
price_tool = FunctionTool.from_defaults(fn=get_current_price)
guideline_tool = FunctionTool.from_defaults(fn=check_guideline)

planner = ClassroomPlanner()
agent = ReActAgent(tools=[price_tool, guideline_tool], llm=planner)


async def run_agent() -> str:
    return str(await agent.run("Can Alice raise AAPL to 36% of the portfolio?"))


agent_result = asyncio.run(run_agent())
# #endregion agent

agent_summary = {
    "framework": "LlamaIndex",
    "agent_class": agent.__class__.__name__,
    "tools": ["get_current_price", "check_guideline"],
    "loop_limit": "max_iterations",
    "model_calls": planner.calls,
}

print("LlamaIndex agent shape:", agent_summary)
print("Agent result:", agent_result)
