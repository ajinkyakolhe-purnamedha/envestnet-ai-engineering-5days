"""Run the M12 starter through a real local MCP stdio connection."""

import asyncio
import json
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from labs.m12_governed_mcp.host_admission import (
    TOOL_NAME,
    admitted_tools,
    admission_denial,
)

SCENARIOS = (
    ("ALICE", {"client_email": "alice@example.com", "max_positions": 2}),
    ("UNASSIGNED", {"client_email": "unassigned@example.com", "max_positions": 2}),
    ("OVER_LIMIT", {"client_email": "alice@example.com", "max_positions": 3}),
)


def _payload(result) -> dict:
    text = result.content[0].text if result.content else "No MCP response content."
    if result.is_error:
        return {"status": "not_implemented", "error": text}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"status": "invalid_mcp_response", "error": text}


async def main() -> None:
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "labs.m12_governed_mcp.server"],
        env={**os.environ, "M12_CALLER": "advisor_01"},
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            discovered = {tool.name for tool in tools.tools}
            print("DISCOVERED:", json.dumps(sorted(discovered)))
            print("MODEL_VISIBLE:", json.dumps(admitted_tools(discovered)))

            excluded = admission_denial("export_all_holdings")
            assert excluded is not None
            print("EXCLUDED_TOOL:", json.dumps(excluded))

            for label, arguments in SCENARIOS:
                admission = admission_denial(TOOL_NAME)
                if admission is not None:
                    print(f"{label}:", json.dumps(admission))
                    continue
                result = await session.call_tool(TOOL_NAME, arguments)
                print(f"{label}:", json.dumps(_payload(result)))


if __name__ == "__main__":
    asyncio.run(main())
