"""M15: a real local model call emits a trace for an operating decision."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from advisor_runtime import run_advisor

advisor_run = run_advisor("Why is a 42% holding above the concentration limit?")
print("Trace:", json.dumps(advisor_run["trace"], sort_keys=True))
print("Status:", advisor_run["status"])
print("Answer:", advisor_run["answer"] or "No answer generated.")
