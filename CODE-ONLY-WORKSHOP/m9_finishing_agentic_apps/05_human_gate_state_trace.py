import json
import os
from datetime import datetime, timezone
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, parse_json_object, print_json


def main() -> None:
    raw_draft = chat([{"role": "user", "content": "Return JSON only with ticker and allocation_pct for: propose AAPL at 36 percent."}], 35)
    draft = parse_json_object(raw_draft)
    verified = isinstance(draft, dict) and isinstance(draft.get("allocation_pct"), (int, float)) and float(draft["allocation_pct"]) <= 35
    state = {"status": "verified" if verified else "draft", "draft": draft, "raw_draft": raw_draft, "trace": [{"at": datetime.now(timezone.utc).isoformat(), "event": "model_draft"}]}
    if verified:
        state["status"] = "awaiting_human_approval"
        if os.getenv("APPROVE") == "true":
            state["status"] = "approved"
            state["trace"].append({"at": datetime.now(timezone.utc).isoformat(), "event": "human_approved"})
    with TemporaryDirectory() as directory:
        path = Path(directory) / "agent-state.json"
        path.write_text(json.dumps(state, indent=2))
        recovered = json.loads(path.read_text())
        print_json("Recovered durable state", {"state_path": str(path), "state": recovered})


if __name__ == "__main__":
    main()
