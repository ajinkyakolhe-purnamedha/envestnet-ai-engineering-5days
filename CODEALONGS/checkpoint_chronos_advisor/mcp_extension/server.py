"""A tiny read-only Chronos MCP server for the checkpoint extension."""

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Chronos Wealth")


@mcp.tool()
def portfolio_summary(client_id: str) -> dict:
    """Return the simulated portfolio for one Chronos investor."""
    portfolios = {
        "alice": {"client": "Alice", "cash": 25_000, "holdings": ["SPY", "QQQ", "GLD"]}
    }
    return portfolios.get(client_id.lower(), {"error": "Unknown demo client."})


@mcp.tool()
def search_policy(query: str) -> dict:
    """Return one matching Chronos investment-policy fact."""
    policy = "No single asset may exceed 35% of the portfolio."
    return {"query": query, "source": "mini_policy.md", "evidence": policy}


if __name__ == "__main__":
    mcp.run(transport="stdio")
