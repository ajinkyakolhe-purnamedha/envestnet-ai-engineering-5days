"""One concept: LlamaIndex workflow drafts are pending rows until approval.

Try:
- Reject both drafts.
- Approve the second draft instead.
- Explain why only approved rows are client-visible after reload.
"""

import json

from llamaindex_closure_setup import ask_llamaindex, m8_workflow_draft


def submit_draft(workflow_output: dict, note: str) -> dict[str, object]:
    return {
        "question": workflow_output["question"],
        "agent_trace_id": "m8-demo-trace-001",
        "note": note,
        "status": "pending",
        "decision_reason": "",
    }


def decide_draft(draft: dict[str, object], decision: str, reason: str) -> dict[str, object]:
    if draft["status"] != "pending":
        raise ValueError("draft already decided")
    draft["status"] = decision
    draft["decision_reason"] = reason
    return draft


def client_visible(drafts: list[dict[str, object]]) -> list[dict[str, object]]:
    return [draft for draft in drafts if draft["status"] == "approved"]


workflow_output = m8_workflow_draft()
generated_draft = ask_llamaindex(
    "Draft one sentence for approval from this agent workflow output:\n"
    f"{workflow_output}",
    max_tokens=40,
)
usable_generated = (
    generated_draft
    and "35%" in generated_draft
    and "workflow output" not in generated_draft.lower()
    and len(generated_draft.split()) <= 30
)
draft_text = generated_draft if usable_generated else workflow_output["draft"]

drafts = [
    submit_draft(workflow_output, draft_text),
    submit_draft(workflow_output, "The portfolio looks fine; no changes needed."),
]
decide_draft(drafts[0], "approved", "clear and cited")
decide_draft(drafts[1], "rejected", "missing threshold")

saved_rows = json.dumps(drafts)
loaded_drafts = json.loads(saved_rows)
published = client_visible(loaded_drafts)

print("saved rows:", saved_rows)
print("client sees:", published)
