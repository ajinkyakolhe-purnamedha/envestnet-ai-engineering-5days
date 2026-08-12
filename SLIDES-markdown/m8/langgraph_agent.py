"""Same agent, LangGraph. The loop becomes a state graph.

Needs GEMINI_API_KEY. Run:
    uv run python -m m8.langgraph_agent
"""

from m8.advisor_tools import (QUESTION, check_guidelines,
                              get_current_price,
                              get_portfolio_allocation)


# #region agent
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

agent = create_agent(
    ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite"),
    tools=[get_current_price,
           get_portfolio_allocation,
           check_guidelines],
    system_prompt=("You are a Chronos Wealth advisor "
                   "assistant. Use the tools to check "
                   "facts before answering."),
)

state = agent.invoke(
    {"messages": [("user", QUESTION)]},
    config={"recursion_limit": 10},
)
print(state["messages"][-1].content)
# #endregion agent


for message in state["messages"]:
    print(type(message).__name__, ":",
          str(message.content)[:60])

# Observed run (gemini-2.5-flash-lite):
#   "Alice cannot raise AAPL to 36% of her portfolio.
#    The guideline is a maximum of 35% ..." with the
#   full trace: Human -> AI(3 tool calls) -> 3 Tool
#   messages -> final AI answer.
#
# LangGraph's word for M7's `messages` list is "state",
# and its word for your `for turn in range(5)` is a graph
# edge that loops agent -> tools -> agent until there are
# no tool calls left. recursion_limit is your max_turns.
# Most control of the four frameworks, most vocabulary to
# learn -- and the industry default, which is why it gets
# a slide even though we build in smolagents.
