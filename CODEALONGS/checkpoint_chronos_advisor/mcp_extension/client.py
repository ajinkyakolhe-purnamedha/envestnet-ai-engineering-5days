"""Connect to the local Chronos MCP server and call its read-only tools."""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server = Path(__file__).with_name("server.py")
    params = StdioServerParameters(command=sys.executable, args=[str(server)])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Discovered tools:", [tool.name for tool in tools.tools])

            portfolio = await session.call_tool("portfolio_summary", {"client_id": "alice"})
            policy = await session.call_tool("search_policy", {"query": "concentration limit"})
            print("Portfolio:", portfolio.content[0].text)
            print("Policy evidence:", policy.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
