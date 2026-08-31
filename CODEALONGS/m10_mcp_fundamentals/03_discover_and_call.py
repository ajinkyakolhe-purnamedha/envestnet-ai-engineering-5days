"""One concept: an MCP client discovers and calls a separate server process."""

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
            tools = await session.list_tools()
            print("Discovered:", [tool.name for tool in tools.tools])
            result = await session.call_tool("portfolio_summary", {"client_id": "alice"})
            print("Portfolio result:", result.content[0].text)


asyncio.run(main())
