"""Advisor agent: use the same live MCP facts to prepare an internal briefing."""

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
    briefing = generate([
        {"role": "system", "content": "You prepare an internal advisor meeting brief. Do not give client-facing advice."},
        {"role": "system", "content": f"Portfolio from MCP: {portfolio}\nPolicy evidence from MCP: {policy}"},
        {"role": "user", "content": "Draft three review questions and label this as requiring advisor review."},
    ])
    print("Advisor briefing draft:", briefing)


if __name__ == "__main__":
    asyncio.run(main())
