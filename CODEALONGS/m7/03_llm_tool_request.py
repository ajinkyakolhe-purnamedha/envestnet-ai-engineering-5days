"""One concept: tool calling is structured text, not Python execution."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from workshop_agentic_setup import QUESTION, TOOL_SCHEMAS, call_smolm


messages = [
    {
        "role": "system",
        "content": (
            "You are selecting a Python tool for an agent. "
            "Return only JSON. No explanation."
        ),
    },
    {
        "role": "user",
        "content": (
            f"Question: {QUESTION}\n"
            f"Available tools: {TOOL_SCHEMAS}\n"
            'Answer: {"tool": "get_current_price", "args": {"symbol": "AAPL"}}'
        ),
    },
]

fallback_text = '{"tool": "get_current_price", "args": {"symbol": "AAPL"}}'
raw_model_text = call_smolm(messages, max_new_tokens=80) or fallback_text
parse_error = None

try:
    tool_request = json.loads(raw_model_text)
except json.JSONDecodeError as error:
    parse_error = str(error)
    tool_request = json.loads(fallback_text)

print("Raw model text:", raw_model_text)
print("Parsed request:", tool_request)
if parse_error:
    print("Model did not return clean JSON, so the snippet uses the classroom fallback.")
    print("Parse fallback:", parse_error)
print("Important: a tool request is text until Python validates and executes it.")
