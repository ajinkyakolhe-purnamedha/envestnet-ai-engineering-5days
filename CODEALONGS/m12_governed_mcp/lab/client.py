"""Run the lab server through a real local MCP stdio exchange."""

import asyncio
import json
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


TOOL_NAME = "advisor_client_review"


def admit_tool(tool_name: str) -> dict | None:
    """Host policy: only admitted tools can cross the MCP call boundary."""
    # TODO 0: allow only TOOL_NAME. Return None when allowed; otherwise return
    # {"status": "denied", "reason": "tool_not_admitted"}.
    return {"status": "not_ready", "reason": "host_admission_not_implemented"}


async def main() -> None:
    server = Path(__file__).with_name("starter_server.py")
    params = StdioServerParameters(command=sys.executable, args=[str(server)],
                                   env={**os.environ, "M12_CALLER": "advisor_01"})
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            discovered = sorted(tool.name for tool in tools.tools)
            model_visible = sorted(
                tool_name for tool_name in discovered if admit_tool(tool_name) is None
            )
            print("DISCOVERED:", json.dumps(discovered))
            print("MODEL_VISIBLE:", json.dumps(model_visible))

            excluded = admit_tool("export_all_holdings")
            assert excluded is not None
            print("EXCLUDED_TOOL:", json.dumps(excluded))

            for label, arguments in [
                ("ALICE", {"client_id": "alice", "max_positions": 2}),
                ("BOB", {"client_id": "bob", "max_positions": 2}),
                ("OVER_LIMIT", {"client_id": "alice", "max_positions": 3}),
            ]:
                admission = admit_tool(TOOL_NAME)
                if admission is not None:
                    print(f"{label}:", json.dumps(admission))
                    continue
                result = await session.call_tool(TOOL_NAME, arguments)
                # MCP pretty-prints tool JSON; compact it for the progress meter.
                payload = json.loads(result.content[0].text)
                print(f"{label}:", json.dumps(payload))


asyncio.run(main())
