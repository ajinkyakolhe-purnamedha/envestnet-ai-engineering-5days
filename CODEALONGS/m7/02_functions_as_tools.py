"""One concept: a Python function becomes a capability the model may request."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from workshop_agentic_setup import TOOL_SCHEMAS, get_current_price


tool_schema = TOOL_SCHEMAS["get_current_price"]
tool_result = get_current_price(symbol="AAPL")

print("Tool schema:", tool_schema)
print("Tool result:", tool_result)
