"""Small MCP client: start the toy server, discover its tool, then call it."""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server = Path(__file__).with_name("simple_mcp_server.py")
    params = StdioServerParameters(command=sys.executable, args=[str(server)])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:", [tool.name for tool in tools.tools])

            result = await session.call_tool("add", {"a": 2, "b": 3})
            print("2 + 3 =", result.content[0].text)

            greeting = await session.read_resource("greeting://Ada")
            print("Greeting:", greeting.contents[0].text)


asyncio.run(main())
