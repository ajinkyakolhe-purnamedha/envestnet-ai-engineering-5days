"""One concept: an MCP-requested client action becomes a pending approval."""

# The model may draft wording, but it must not deliver the note itself.
proposal = {
    "status": "approval_required",
    "draft": "Explain Alice's concentration risk in plain language.",
    "approver_role": "advisor_supervisor",
    "client_delivery_executed": False,
    "portfolio_mutation_executed": False,
}

# The workflow records what still needs a durable human approval.
for key, value in proposal.items():
    print(f"{key}: {value}")
