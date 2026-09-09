"""M13: a JSON-shaped proposal still needs Python validation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from advisor_contracts import handle_proposal

bad_proposals = [{"client_id": "alice"}, {"kind": "policy_answer", "rows": "all"}, "not JSON"]
for bad_proposal in bad_proposals:
    result = handle_proposal(bad_proposal, evidence_ids=["policy-v1"])
    assert result["status"] == "invalid_model_output"
    print({"proposal": bad_proposal, "result": result})
