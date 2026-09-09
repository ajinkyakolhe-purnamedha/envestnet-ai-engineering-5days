"""M14: deny an exfiltration proposal before any synthetic data read."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_runtime import evaluate_request

attack_request = {"tool": "export_all_holdings", "client_id": "alice", "max_positions": 2}
outcome = evaluate_request(attack_request, caller_id="advisor_01")
assert outcome["status"] == "blocked"
assert outcome["result"] is None
print("Hardened outcome:", outcome)
