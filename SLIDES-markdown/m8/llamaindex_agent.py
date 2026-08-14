"""Same agent, LlamaIndex. Tools first, RAG next door.

Needs GEMINI_API_KEY. Run:
    uv run --project ../CODE-ALONGS \
        python m8/llamaindex_agent.py
"""

import asyncio

from m8.advisor_tools import (QUESTION, check_guidelines,
                              get_current_price,
                              get_portfolio_allocation)


# #region agent
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.google_genai import GoogleGenAI

agent = FunctionAgent(
    tools=[get_current_price,
           get_portfolio_allocation,
           check_guidelines],
    llm=GoogleGenAI(model="gemini-2.5-flash-lite"),
    system_prompt=("You are a Chronos Wealth advisor "
                   "assistant. Use the tools to check "
                   "facts before answering."),
)

async def main():
    return await agent.run(QUESTION)

print(asyncio.run(main()))
# #endregion agent

# Observed run (gemini-2.5-flash-lite):
#   "Alice cannot raise AAPL to 36% of her portfolio.
#    The guideline is a maximum of 35% for any given
#    stock."
#
# Gotcha found while testing: agent.run() must be called
# INSIDE a running event loop (async main + asyncio.run);
# calling it at module level raises "no running event
# loop".
#
# LlamaIndex wraps each plain function in a FunctionTool,
# reading your type hints and docstring as the contract --
# the registry + schema you built by hand in M7.
#
# Why LlamaIndex gets a slide: its agents and its RAG
# machinery share one toolbox. The M4/M5 policy index you
# built on Day 2 becomes just another tool via
# QueryEngineTool -- "your retriever just became a tool"
# is the whole pitch. See llamaindex_rag_agent.py.
