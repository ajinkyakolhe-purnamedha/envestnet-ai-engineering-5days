"""One concept: Python validates and dispatches the model's requested tool."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from workshop_agentic_setup import TOOL_FUNCTIONS


model_text = '{"tool": "get_current_price", "args": {"symbol": "AAPL"}}'
tool_request = json.loads(model_text)

tool_name = tool_request["tool"]
args = tool_request["args"]

if tool_name not in TOOL_FUNCTIONS:
    raise ValueError(f"Unknown tool: {tool_name}")

result = TOOL_FUNCTIONS[tool_name](**args)
observation = {"tool": tool_name, "args": args, "result": result}

print("Tool request:", tool_request)
print("Observation:", observation)
