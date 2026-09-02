"""One concept: a live local model runs under a LlamaIndex step limit."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core.agent.workflow import ReActAgent, ToolCallResult
from llama_index.core.tools import FunctionTool

from local_hf_agent import LocalSmolFunctionLLM
from workshop_framework_setup import get_current_price

llm = LocalSmolFunctionLLM()
agent = ReActAgent(
    tools=[FunctionTool.from_defaults(fn=get_current_price)],
    llm=llm,
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
runtime = {
    "backend": "local Hugging Face inference",
    "model": llm.metadata.model_name,
    "model_calls": llm.generation_count,
    "latency_ms": llm.last_generation_latency_ms,
    "max_iterations": 3,
}

print("Runtime:", runtime)
print("Raw model text:", llm.last_response)
print("Trace:")
for item in trace:
    print(item)
print("Blocked:", blocked)
