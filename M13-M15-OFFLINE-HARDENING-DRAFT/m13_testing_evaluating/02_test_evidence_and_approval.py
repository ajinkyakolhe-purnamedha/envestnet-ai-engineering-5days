"""M13: absence of evidence abstains; client-visible drafts wait for a human."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from advisor_contracts import handle_proposal

missing_evidence = handle_proposal({"kind": "policy_answer"}, evidence_ids=[])
pending_draft = handle_proposal({"kind": "draft"}, evidence_ids=["policy-v1"])
assert missing_evidence["status"] == "needs_evidence"
assert pending_draft["status"] == "approval_required"
print({"without_evidence": missing_evidence, "draft": pending_draft})
