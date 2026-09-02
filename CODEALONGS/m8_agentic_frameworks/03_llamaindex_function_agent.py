"""One concept: LlamaIndex runs a real local Hugging Face tool-calling agent."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "m4_building_rags"))

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.agent.workflow import ToolCallResult
from llama_index.core.tools import FunctionTool

from workshop_framework_setup import check_guideline, get_current_price
from local_hf_agent import LocalSmolFunctionLLM


price_tool = FunctionTool.from_defaults(fn=get_current_price)
guideline_tool = FunctionTool.from_defaults(fn=check_guideline)
llama_tools = [price_tool, guideline_tool]
tool_names = [item.metadata.name for item in llama_tools]

llm = LocalSmolFunctionLLM()
agent = FunctionAgent(
    tools=llama_tools,
    llm=llm,
    streaming=False,
    system_prompt="Use the available tools to answer the user's question.",
)


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
model_call_count = llm.generation_count
runtime = {
    "backend": "local Hugging Face inference",
    "model": llm.metadata.model_name,
    "model_calls": model_call_count,
    "latency_ms": llm.last_generation_latency_ms,
}

print("Runtime:", runtime)
print("Raw model text:", llm.last_response)
print("LlamaIndex tools:", tool_names)
print("Agent class:", agent.__class__.__name__)
print("Tool trace:", tool_trace)
print("Model calls:", model_call_count)
print("Agent result:", agent_result)
