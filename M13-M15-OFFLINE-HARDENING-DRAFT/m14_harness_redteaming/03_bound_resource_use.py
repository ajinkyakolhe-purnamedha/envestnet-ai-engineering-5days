"""M14: valid-looking repeated work still stops at a deterministic limit."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_runtime import evaluate_request

valid_request = {"tool": "get_portfolio_summary", "client_id": "alice", "max_positions": 1}
contained = evaluate_request(valid_request, caller_id="advisor_01", step_count=3)
assert contained["status"] == "contained"
assert contained["reason"] == "step_limit_reached"
print("Resource-bound outcome:", contained)
print("This is application-level containment, not an operating-system sandbox.")
