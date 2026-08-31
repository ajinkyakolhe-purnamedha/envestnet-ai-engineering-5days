"""Investor agent: use live MCP facts to create an educational explanation."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from chronos_client import call_chronos_tools
from offline_model import generate


async def main() -> None:
    portfolio, policy = await call_chronos_tools([
        ("portfolio_summary", {"client_id": "alice"}),
        ("search_policy", {"query": "concentration limit"}),
    ])
    reply = generate([
        {"role": "system", "content": "You are an educational investor assistant. Explain facts; do not recommend trades."},
        {"role": "system", "content": f"Portfolio from MCP: {portfolio}\nPolicy evidence from MCP: {policy}"},
        {"role": "user", "content": "Explain diversification and the concentration policy in plain language."},
    ])
    print("Investor explanation:", reply)


if __name__ == "__main__":
    asyncio.run(main())
