"""Progress meter for Lab 12. It fails until the learner completes the policy."""

import json
from pathlib import Path
import subprocess
import sys


client = Path(__file__).with_name("client.py")
run = subprocess.run([sys.executable, str(client)], capture_output=True, text=True)
if run.returncode:
    raise SystemExit(run.stderr)


def response(label: str) -> dict:
    line = next(line for line in run.stdout.splitlines() if line.startswith(f"{label}:"))
    return json.loads(line.split(":", 1)[1])


alice, bob, over_limit = response("ALICE"), response("BOB"), response("OVER_LIMIT")
excluded_tool = response("EXCLUDED_TOOL")
checks = {
    "discovery": 'DISCOVERED: ["advisor_client_review", "export_all_holdings"]' in run.stdout,
    "host admission before dispatch": (
        'MODEL_VISIBLE: ["advisor_client_review"]' in run.stdout
        and excluded_tool == {"status": "denied", "reason": "tool_not_admitted"}
    ),
    "bounded Alice read": alice.get("status") == "ok" and len(alice.get("holdings", [])) == 2,
    "Bob denied before read": bob.get("reason") == "unassigned_client",
    "over-limit request denied": over_limit.get("reason") == "max_positions_must_be_1_or_2",
    "audit evidence": all("correlation_id" in item.get("audit", {}) for item in [alice, bob, over_limit]),
}

for name, passed in checks.items():
    print(f"{'PASS' if passed else 'TODO'}: {name}")

if not all(checks.values()):
    raise SystemExit("Complete TODO 0 in client.py and TODOs 1–3 in starter_server.py.")
