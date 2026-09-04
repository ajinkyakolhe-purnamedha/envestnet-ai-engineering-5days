"""One concept: server policy checks scope before it reads data."""

# A verified advisor identity has an assignment. In production, the host
# authenticates this identity; a role written in a prompt would not be enough.
assigned_clients = {"advisor_01": {"alice"}}


def read_client_review(client_id: str) -> dict:
    return {"client_id": client_id, "largest_position": "SPY"}


def request_review(caller_id: str, client_id: str) -> None:
    # The model may request Bob, but Python checks authority before this call.
    if client_id not in assigned_clients[caller_id]:
        print(f"DENY {client_id}: unassigned_client; read service not called")
        return
    # Only an allowed request reaches the deterministic data service.
    print(f"ALLOW {client_id}: read service called", read_client_review(client_id))


request_review("advisor_01", "alice")
request_review("advisor_01", "bob")
