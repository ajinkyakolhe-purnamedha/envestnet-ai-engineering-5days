"""One concept: two applications reuse live MCP facts in real model calls."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


CHECKPOINT_DIR = Path(__file__).resolve().parents[1] / "checkpoint_chronos_advisor"
sys.path.insert(0, str(CHECKPOINT_DIR))
from offline_model import generate


def investor_messages(portfolio: str, policy: str) -> list[dict[str, str]]:
    """Use shared facts for an education-only investor explanation."""
    return [
        {
            "role": "system",
            "content": (
                "You are an educational investor assistant. Explain only the "
                "supplied facts. Do not recommend trades."
            ),
        },
        {
            "role": "system",
            "content": f"Portfolio from MCP: {portfolio}\nPolicy from MCP: {policy}",
        },
        {"role": "user", "content": "Explain diversification in plain language."},
    ]


def advisor_messages(portfolio: str, policy: str) -> list[dict[str, str]]:
    """Use the same facts for an internal advisor preparation draft."""
    return [
        {
            "role": "system",
            "content": (
                "You prepare an internal meeting draft for an advisor. Use only "
                "the supplied facts. Do not send a client-facing message or trade."
            ),
        },
        {
            "role": "system",
            "content": f"Portfolio from MCP: {portfolio}\nPolicy from MCP: {policy}",
        },
        {
            "role": "user",
            "content": "Draft a short internal meeting note about concentration risk.",
        },
    ]


async def shared_facts() -> tuple[str, str]:
    """Run the same MCP tool calls any independent host application can make."""
    server = Path(__file__).with_name("02_chronos_mcp_server.py")
    params = StdioServerParameters(command=sys.executable, args=[str(server)])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            portfolio = await session.call_tool("portfolio_summary", {"client_id": "alice"})
            policy = await session.call_tool("search_policy", {"query": "concentration limit"})
            return portfolio.content[0].text, policy.content[0].text


async def main() -> None:
    investor_portfolio, investor_policy = await shared_facts()
    investor_reply = generate(investor_messages(investor_portfolio, investor_policy))

    advisor_portfolio, advisor_policy = await shared_facts()
    advisor_draft = generate(advisor_messages(advisor_portfolio, advisor_policy))

    print("Investor Education App:", investor_reply)
    print("Advisor Preparation App:", advisor_draft)


if __name__ == "__main__":
    asyncio.run(main())
