"""M13: the same boundary expressed as small repeatable pytest tests."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from advisor_contracts import handle_proposal


def test_grounded_policy_answer_requires_evidence():
    assert handle_proposal({"kind": "policy_answer"}, ["policy-v1"])["status"] == "complete"
    assert handle_proposal({"kind": "policy_answer"}, [])["status"] == "needs_evidence"


def test_client_visible_content_starts_pending_human_review():
    assert handle_proposal({"kind": "draft"}, ["policy-v1"])["status"] == "approval_required"
