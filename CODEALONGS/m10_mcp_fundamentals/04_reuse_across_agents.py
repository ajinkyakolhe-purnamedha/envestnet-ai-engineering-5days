"""One concept: two applications reuse the same live MCP capabilities."""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server = Path(__file__).with_name("02_chronos_mcp_server.py")
    params = StdioServerParameters(command=sys.executable, args=[str(server)])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            portfolio = await session.call_tool("portfolio_summary", {"client_id": "alice"})
            policy = await session.call_tool("search_policy", {"query": "concentration limit"})
            print("Investor agent: explain these facts to Alice.")
            print(portfolio.content[0].text)
            print("Advisor agent: prepare an internal review using the same facts.")
            print(policy.content[0].text)


asyncio.run(main())
