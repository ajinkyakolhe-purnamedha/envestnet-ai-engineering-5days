"""One concept: an MCP server enforces scope before it returns Chronos facts."""

import logging
import os
import sys
from uuid import uuid4

from mcp.server import MCPServer


logging.basicConfig(stream=sys.stderr, level=logging.INFO)
mcp = MCPServer("Chronos Governed MCP")
# In a real application, this identity arrives from authenticated host context.
ASSIGNED_CLIENTS = {"advisor_01": {"alice"}}
PORTFOLIOS = {"alice": ["SPY", "QQQ", "GLD"]}
AUDIT_EVENTS = []  # Classroom stand-in for a durable audit sink.


def audit(caller_id: str, decision: str, executed: bool) -> dict:
    """Record only the policy evidence needed to investigate this call."""
    event = {"correlation_id": uuid4().hex[:8], "caller": caller_id,
             "tool": "advisor_client_review", "decision": decision,
             "downstream_executed": executed}
    AUDIT_EVENTS.append(event)
    logging.info("audit=%s", event)
    return event


@mcp.tool()
def advisor_client_review(client_id: str, max_positions: int = 2) -> dict:
    """Return a bounded review only for the caller's assigned client."""
    # The classroom client supplies this fixture; it is not a user/model claim.
    caller_id = os.environ.get("M12_CALLER", "unknown")  # Classroom fixture.
    # Authorization happens before data access: Bob's facts are never read.
    if client_id not in ASSIGNED_CLIENTS.get(caller_id, set()):
        return {"status": "denied", "reason": "unassigned_client", "audit": audit(caller_id, "deny", False)}
    # A permitted caller still cannot ask for unlimited model context.
    if not 1 <= max_positions <= 2:
        return {"status": "denied", "reason": "max_positions_exceeded", "audit": audit(caller_id, "deny", False)}

    # This is the first line that reads Chronos facts, after both policy checks.
    holdings = PORTFOLIOS[client_id][:max_positions]
    return {
        "status": "ok", "client_id": client_id, "holdings": holdings,
        "simulated_date": "2026-08-29", "audit": audit(caller_id, "allow", True),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
