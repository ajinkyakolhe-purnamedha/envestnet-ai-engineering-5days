"""One concept: LlamaIndex owns a real local-model tool-calling loop."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core.agent.workflow import FunctionAgent, ToolCallResult
from llama_index.core.tools import FunctionTool

from local_hf_agent import LocalSmolFunctionLLM
from workshop_framework_setup import get_current_price


price_tool = FunctionTool.from_defaults(fn=get_current_price)
llm = LocalSmolFunctionLLM()
agent = FunctionAgent(tools=[price_tool], llm=llm, streaming=False)


async def run_agent() -> tuple[str, list[str]]:
    handler = agent.run("What is the current price of AAPL?", max_iterations=3)
    tool_trace = []
    try:
        async for event in handler.stream_events():
            if isinstance(event, ToolCallResult):
                tool_trace.append(event.tool_name)
        return str(await handler), tool_trace
    except Exception as error:
        return f"{type(error).__name__}: {error}", tool_trace


agent_result, tool_trace = asyncio.run(run_agent())
agent_summary = {
    "framework": "LlamaIndex",
    "agent_class": agent.__class__.__name__,
    "tools": [price_tool.metadata.name],
    "model": llm.metadata.model_name,
    "model_calls": llm.generation_count,
    "tool_trace": tool_trace,
}
runtime = {
    "backend": "local Hugging Face inference",
    "model": llm.metadata.model_name,
    "model_calls": llm.generation_count,
    "latency_ms": llm.last_generation_latency_ms,
}

print("Runtime:", runtime)
print("Raw model text:", llm.last_response)
print("LlamaIndex agent shape:", agent_summary)
print("Agent result:", agent_result)
