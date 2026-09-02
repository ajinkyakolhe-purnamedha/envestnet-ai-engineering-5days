"""One concept: MCP publishes existing Python capabilities as tools."""

from mcp.server import MCPServer

mcp = MCPServer("Chronos Wealth")


@mcp.tool()
def portfolio_summary(client_id: str) -> dict:
    """Return a simulated investor portfolio.

    Args:
        client_id: Demo client identifier, for example alice.
    """
    return {"client": client_id, "cash": 25_000, "holdings": ["SPY", "QQQ", "GLD"]}


@mcp.tool()
def search_policy(query: str) -> dict:
    """Return one Chronos policy fact.

    Args:
        query: The policy question to search.
    """
    return {"query": query, "source": "mini_policy.md", "evidence": "No single asset may exceed 35% of the portfolio."}


if __name__ == "__main__":
    mcp.run(transport="stdio")
