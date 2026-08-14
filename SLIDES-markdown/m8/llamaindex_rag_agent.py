"""The Day 2 pitch: your retriever just became a tool.

Needs GEMINI_API_KEY. Run:
    uv run --project ../CODE-ALONGS \
        python m8/llamaindex_rag_agent.py
"""

import asyncio
from pathlib import Path

from m8.advisor_tools import check_guidelines


# #region agent
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.google_genai import GoogleGenAI

POLICY = Path("data/investment_policy.md").read_text()


def search_investment_policy(query: str) -> str:
    """Return policy paragraphs that mention query words."""
    words = {w.lower() for w in query.split()}
    hits = [p for p in POLICY.split("\n\n")
            if words & set(p.lower().split())]
    return "\n\n".join(hits[:3]) or "No matching policy."


agent = FunctionAgent(
    tools=[search_investment_policy, check_guidelines],
    llm=GoogleGenAI(model="gemini-2.5-flash-lite"),
    system_prompt=("Answer advisor questions using the "
                   "policy search tool. Cite the policy "
                   "text you relied on."),
)

async def main():
    return await agent.run(
        "What does our policy say about concentration "
        "risk, and is 36% in one stock allowed?")

print(asyncio.run(main()))
# #endregion agent

# Observed run (gemini-2.5-flash-lite):
#   "The policy states that no single holding may exceed
#    35% of total portfolio value. Therefore, 36% in one
#    stock is not allowed."
#
# In M4 you built retrieval as a pipeline the user walks
# through once: query -> chunks -> answer. Here the SAME
# retrieval is a tool the agent calls when IT decides the
# question needs policy text -- and it can combine it
# with check_guidelines in one run. RAG stops being an
# architecture and becomes a capability. (In production,
# swap the keyword function for the M4/M5 vector index
# behind a QueryEngineTool -- the agent code is
# unchanged.)
