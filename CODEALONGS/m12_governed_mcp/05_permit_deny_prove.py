"""One concept: a real MCP client can prove an allowed call and safe denial."""

import asyncio
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    # This client starts a separate process; it does not import the server.
    server = Path(__file__).with_name("04_governed_chronos_server.py")
    # The environment value is a classroom stand-in for a verified identity.
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(server)],
        env={**os.environ, "M12_CALLER": "advisor_01"},
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            # First learn what the server publishes through the MCP protocol.
            await session.initialize()
            tools = await session.list_tools()
            print("Discovered:", [tool.name for tool in tools.tools])

            # Alice is assigned to advisor_01, so the server permits this read.
            allowed = await session.call_tool(
                "advisor_client_review", {"client_id": "alice", "max_positions": 2}
            )
            # Bob is not assigned. The server denies this before reading data.
            denied = await session.call_tool(
                "advisor_client_review", {"client_id": "bob", "max_positions": 2}
            )
            print("ALLOW:", allowed.content[0].text)
            print("DENY:", denied.content[0].text)


asyncio.run(main())
