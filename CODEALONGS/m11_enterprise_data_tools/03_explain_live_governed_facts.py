"""One concept: audience changes workflow, not the trusted MCP facts.

Run with `--audience investor` or `--audience advisor`.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

CHECKPOINT_DIR = Path(__file__).resolve().parents[1] / "checkpoint_chronos_advisor"
sys.path.insert(0, str(CHECKPOINT_DIR))
from offline_model import generate


def investor_messages(portfolio: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": "You are an educational Chronos investor assistant. Explain only the supplied facts. Do not recommend trades."},
        {"role": "system", "content": f"Investor portfolio result from MCP:\n{portfolio}"},
        {"role": "user", "content": "Explain my portfolio in plain language."},
    ]


def advisor_messages(review: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": "You prepare an internal review draft for an advisor. Use only the supplied facts. Do not trade or send a client-facing message."},
        {"role": "system", "content": f"Advisor review result from MCP:\n{review}"},
        {"role": "user", "content": "Draft a short concentration-risk review note."},
    ]


async def call_tool(tool_name: str, arguments: dict) -> str:
    server = Path(__file__).with_name("02_chronos_data_server.py")
    params = StdioServerParameters(command=sys.executable, args=[str(server)])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return result.content[0].text


async def main(audience: str) -> None:
    if audience == "investor":
        facts = await call_tool("investor_portfolio_view", {"client_id": "alice", "max_positions": 2})
        print("Investor MCP facts:", facts)
        print("Investor education explanation:", generate(investor_messages(facts), max_new_tokens=100))
        return

    facts = await call_tool("advisor_client_review", {"client_id": "alice"})
    draft = {"status": "pending", "audience": "advisor", "note": generate(advisor_messages(facts), max_new_tokens=100)}
    print("Advisor MCP facts:", facts)
    print("Pending internal advisor draft:", draft)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audience", choices=("investor", "advisor"), default="investor")
    asyncio.run(main(parser.parse_args().audience))
