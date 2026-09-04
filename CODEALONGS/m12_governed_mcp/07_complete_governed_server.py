"""Final walkthrough: a small MCP server with deterministic governance.

Run this through 08_complete_walkthrough.py; stdout is reserved for MCP.
"""

import logging
import os
import sys
from uuid import uuid4

from mcp.server import MCPServer


logging.basicConfig(stream=sys.stderr, level=logging.INFO)
mcp = MCPServer("Chronos Complete Governed MCP")
ASSIGNED = {"advisor_01": {"alice"}}
POSITIONS = {"alice": ["SPY", "QQQ", "GLD"]}
AUDIT_EVENTS = []  # Classroom stand-in for a durable audit store.


def record(caller: str, decision: str, executed: bool) -> dict:
    """Store sanitized evidence, never a full portfolio or secret."""
    event = {"correlation_id": uuid4().hex[:8], "caller": caller,
             "decision": decision, "downstream_executed": executed}
    AUDIT_EVENTS.append(event)
    logging.info("audit=%s", event)  # stderr is safe; stdout is MCP traffic.
    return event


def denied(caller: str, reason: str) -> dict:
    return {"status": "denied", "reason": reason, "audit": record(caller, "deny", False)}


@mcp.tool()
def advisor_client_review(client_id: str, max_positions: int = 2) -> dict:
    """Return a bounded review for an assigned client only."""
    caller = os.environ.get("M12_CALLER", "unknown")  # Verified-host fixture.
    if client_id not in ASSIGNED.get(caller, set()):
        return denied(caller, "unassigned_client")  # No data read.
    if max_positions not in {1, 2}:
        return denied(caller, "max_positions_must_be_1_or_2")
    return {"status": "ok", "holdings": POSITIONS[client_id][:max_positions],
            "simulated_date": "2026-08-29", "audit": record(caller, "allow", True)}


@mcp.tool()
def prepare_client_note(client_id: str) -> dict:
    """Create a pending draft, never a client delivery or portfolio mutation."""
    caller = os.environ.get("M12_CALLER", "unknown")
    if client_id not in ASSIGNED.get(caller, set()):
        return denied(caller, "unassigned_client")
    return {"status": "approval_required", "approver_role": "advisor_supervisor",
            "client_delivery_executed": False, "audit": record(caller, "pending_approval", False)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
