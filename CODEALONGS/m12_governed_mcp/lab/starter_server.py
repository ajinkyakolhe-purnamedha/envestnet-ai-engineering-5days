"""Lab starter: complete the server checks, then run client.py.

This is a real local MCP server. The `not_ready` response is intentional until
the learner fills the three labelled policy gaps.
"""

import logging
import os
import sys

from mcp.server import MCPServer


logging.basicConfig(stream=sys.stderr, level=logging.INFO)
mcp = MCPServer("Chronos M12 Lab")
ASSIGNED_CLIENTS = {"advisor_01": {"alice"}}
PORTFOLIOS = {"alice": ["SPY", "QQQ", "GLD"]}
AUDIT_EVENTS = []


def read_client_review(client_id: str, max_positions: int) -> dict:
    """This data read must happen only after both policy checks."""
    return {"client_id": client_id, "holdings": PORTFOLIOS[client_id][:max_positions]}


def audit(caller: str, decision: str, executed: bool) -> dict:
    # TODO 3: create a sanitized event, append it, log it to stderr, return it.
    # Required keys: correlation_id, caller, tool, decision, downstream_executed.
    return {"status": "not_ready"}


@mcp.tool()
def advisor_client_review(client_id: str, max_positions: int = 2) -> dict:
    """Return a bounded review only for this caller's assigned client."""
    caller = os.environ.get("M12_CALLER", "unknown")  # Trusted-host fixture.

    # TODO 1: deny an unassigned client before read_client_review can run.
    # Return status=denied, reason=unassigned_client, and a deny audit event.

    # TODO 2: deny max_positions unless it is 1 or 2, before the data read.
    # Use reason=max_positions_must_be_1_or_2 and a deny audit event.

    # Replace this temporary result with a bounded read and an allow audit event.
    return {"status": "not_ready", "caller": caller}


if __name__ == "__main__":
    mcp.run(transport="stdio")
