"""M12 map: one safe request path in ordinary Python, before real MCP code."""

# This snippet is a map. Snippets 04/05 repeat the same decisions over real MCP.
approved_tools = {"advisor_client_review"}
assigned_clients = {"advisor_01": {"alice"}}


def request_review(client_id: str) -> None:
    print(f"\nModel proposes: advisor_client_review({client_id!r})")

    # Host policy decides which discovered tools the model may call.
    if "advisor_client_review" not in approved_tools:
        print("DENY: tool_not_approved")
        return

    # Server policy checks scope before the data service can run.
    if client_id not in assigned_clients["advisor_01"]:
        print(f"DENY {client_id}: unassigned_client; no data read")
        return

    # A permitted request receives bounded deterministic facts, not a trade.
    print(f"ALLOW {client_id}: bounded Chronos facts", {"holdings": ["SPY", "QQQ"]})
    print("AUDIT: decision=allow, downstream_executed=True")


request_review("alice")
request_review("bob")
print("\nNext: make this same path real over MCP in 04/05.")
