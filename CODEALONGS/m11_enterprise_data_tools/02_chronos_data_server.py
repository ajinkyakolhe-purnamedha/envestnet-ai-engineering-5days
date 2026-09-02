"""One concept: MCP publishes business contracts over miniature Chronos services."""

from mcp.server import MCPServer

from governed_data_product import build_current_portfolio_snapshot, generate_advisor_review_report


mcp = MCPServer("Chronos Governed Data")


@mcp.tool()
def investor_portfolio_view(client_id: str, max_positions: int = 3) -> dict:
    """Return a bounded investor portfolio view with simulated-date provenance."""
    try:
        return build_current_portfolio_snapshot(client_id, max_positions)
    except ValueError as error:
        return {"status": "invalid_input", "message": str(error)}


@mcp.tool()
def advisor_client_review(client_id: str) -> dict:
    """Return deterministic concentration metrics for an internal advisor review."""
    return generate_advisor_review_report(client_id)


if __name__ == "__main__":
    mcp.run(transport="stdio")
