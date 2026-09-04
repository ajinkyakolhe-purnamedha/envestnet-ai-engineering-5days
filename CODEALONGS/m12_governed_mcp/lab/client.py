"""Run the lab server through a real local MCP stdio exchange."""

import asyncio
import json
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server = Path(__file__).with_name("starter_server.py")
    params = StdioServerParameters(command=sys.executable, args=[str(server)],
                                   env={**os.environ, "M12_CALLER": "advisor_01"})
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("DISCOVERED:", json.dumps([tool.name for tool in tools.tools]))
            for label, arguments in [
                ("ALICE", {"client_id": "alice", "max_positions": 2}),
                ("BOB", {"client_id": "bob", "max_positions": 2}),
                ("OVER_LIMIT", {"client_id": "alice", "max_positions": 3}),
            ]:
                result = await session.call_tool("advisor_client_review", arguments)
                # MCP pretty-prints tool JSON; compact it for the progress meter.
                payload = json.loads(result.content[0].text)
                print(f"{label}:", json.dumps(payload))


asyncio.run(main())
