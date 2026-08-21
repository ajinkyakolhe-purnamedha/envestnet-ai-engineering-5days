"""One concept: LlamaIndex wraps Python functions as FunctionTool objects."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "m4"))

from llama_index.core import Settings
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool

from workshop_framework_setup import check_guideline, get_current_price
from workshop_llamaindex_setup import use_local_models


use_local_models()

price_tool = FunctionTool.from_defaults(fn=get_current_price)
guideline_tool = FunctionTool.from_defaults(fn=check_guideline)
llama_tools = [price_tool, guideline_tool]
tool_names = [item.metadata.name for item in llama_tools]

agent = FunctionAgent(
    tools=llama_tools,
    llm=Settings.llm,
    system_prompt="Use tools for market data and guideline checks before answering.",
)

print("LlamaIndex tools:", tool_names)
print("Agent class:", agent.__class__.__name__)
