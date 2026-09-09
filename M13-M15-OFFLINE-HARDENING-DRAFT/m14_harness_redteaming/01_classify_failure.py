"""M14: classify the failure before choosing a control."""

failure_to_remedy = {
    "prompt_injection": "Do not trust instruction text; admit only explicit capabilities.",
    "tool_or_context": "Validate request shape and scope before the data read.",
    "architecture": "Use Python policy gates, bounded results, and audit events.",
    "knowledge_gap": "Retrieve an approved source or abstain; do not invent facts.",
}
for failure, remedy in failure_to_remedy.items():
    print({"failure": failure, "remedy": remedy})
