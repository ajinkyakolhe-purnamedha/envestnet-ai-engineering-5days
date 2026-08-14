"""Persistence is a row, in miniature.

First run: queue two drafts, then the process 'dies'.
Second run: the pending drafts are still there — resume and
decide one. A variable dies with its process; a file (or a
table) survives it. Delete pending_drafts.json to reset.
Run twice from SLIDES-markdown/:
    uv run --project ../CODE-ALONGS python m9/state_resume.py
"""

import json
from pathlib import Path

# #region resume
STATE = Path(__file__).parent / "pending_drafts.json"


def load_pending() -> list[str]:
    if STATE.exists():
        return json.loads(STATE.read_text())
    return []


def save_pending(drafts: list[str]) -> None:
    STATE.write_text(json.dumps(drafts))


pending = load_pending()
if not pending:
    pending = ["draft note for Alice", "draft note for Bob"]
    save_pending(pending)
    print("queued 2 drafts... and the process died here.")
    print("run me again: did the queue survive?")
    raise SystemExit

print(f"restart: {len(pending)} pending drafts survived")
approved = pending.pop(0)
save_pending(pending)
print(f"approved '{approved}'; {len(pending)} still pending")
# #endregion resume
