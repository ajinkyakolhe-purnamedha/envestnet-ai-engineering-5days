"""M15: trace evidence identifies the layer to repair."""

failed_trace = {"status": "needs_evidence", "evidence_ids": [], "policy_decision": "abstain_missing_evidence"}
healthy_trace = {"status": "complete", "evidence_ids": ["policy/concentration-limit-v1"], "policy_decision": "answer_allowed"}
diagnosis = "retrieval_or_context" if not failed_trace["evidence_ids"] else "unknown"
print({"failed": failed_trace, "healthy": healthy_trace, "diagnosis": diagnosis})
print("Repair the missing evidence layer, not the model prompt.")
