"""Python-owned contracts used to test an uncertain advisor boundary."""

from __future__ import annotations


def handle_proposal(proposal: object, evidence_ids: list[str], max_steps: int = 2) -> dict[str, object]:
    """Validate model-shaped input; never let it calculate or approve anything."""

    if not isinstance(proposal, dict) or proposal.get("kind") not in {"policy_answer", "draft"}:
        return {"status": "invalid_model_output", "audit": "proposal_rejected"}
    if set(proposal) != {"kind"}:
        return {"status": "invalid_model_output", "audit": "unexpected_fields"}
    if proposal["kind"] == "policy_answer" and not evidence_ids:
        return {"status": "needs_evidence", "audit": "retrieval_empty"}
    if proposal["kind"] == "draft":
        return {"status": "approval_required", "audit": "draft_pending_human_review"}
    if max_steps < 1:
        return {"status": "max_steps_reached", "audit": "step_budget_reached"}
    return {"status": "complete", "audit": "grounded_policy_answer", "evidence_ids": evidence_ids}
