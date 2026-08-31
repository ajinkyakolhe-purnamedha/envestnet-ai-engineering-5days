"""One small MCP client helper shared by the two Chronos agent examples."""

import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def call_chronos_tools(calls: list[tuple[str, dict]]) -> list[str]:
    """Start the local MCP server and return the text from each tool call."""
    server = Path(__file__).with_name("server.py")
    params = StdioServerParameters(command=sys.executable, args=[str(server)])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return [
                (await session.call_tool(tool_name, arguments)).content[0].text
                for tool_name, arguments in calls
            ]
