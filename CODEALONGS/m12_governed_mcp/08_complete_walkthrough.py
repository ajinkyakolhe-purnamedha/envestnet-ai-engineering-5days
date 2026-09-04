"""Run the final governed server and inspect every decision in one place."""

import asyncio
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server = Path(__file__).with_name("07_complete_governed_server.py")
    params = StdioServerParameters(command=sys.executable, args=[str(server)],
                                   env={**os.environ, "M12_CALLER": "advisor_01"})
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            discovered = await session.list_tools()
            approved = {"advisor_client_review", "prepare_client_note"}
            names = sorted(tool.name for tool in discovered.tools)
            print("Discovered:", names)
            print("Host admits:", sorted(set(names) & approved))

            async def call(name: str, arguments: dict) -> str:
                return (await session.call_tool(name, arguments)).content[0].text

            print("ALLOW:", await call("advisor_client_review", {"client_id": "alice"}))
            print("DENY:", await call("advisor_client_review", {"client_id": "bob"}))
            print("APPROVAL:", await call("prepare_client_note", {"client_id": "alice"}))


asyncio.run(main())
