"""One concept: ReAct repeats plan, act, observe until final or max_turns."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from workshop_agentic_setup import QUESTION, TOOL_FUNCTIONS, summarize_guideline


def planner(state: dict) -> dict:
    """Deterministic stand-in for the LLM planner."""

    tools_seen = {item["tool"] for item in state["observations"]}
    if "get_current_price" not in tools_seen:
        return {"thought": "Need current market data.", "tool": "get_current_price", "args": {"symbol": "AAPL"}}
    if "get_portfolio_allocation" not in tools_seen:
        return {
            "thought": "Need Alice's current exposure.",
            "tool": "get_portfolio_allocation",
            "args": {"client": "Alice", "symbol": "AAPL"},
        }
    if "check_guideline" not in tools_seen:
        return {
            "thought": "Need to compare 36% with the concentration limit.",
            "tool": "check_guideline",
            "args": {"symbol": "AAPL", "proposed_allocation_pct": 36.0},
        }

    guideline = next(item["result"] for item in state["observations"] if item["tool"] == "check_guideline")
    return {"thought": "All facts are available.", "final": summarize_guideline(guideline)}


state = {"question": QUESTION, "observations": []}
trace = []
max_turns = 5

for turn in range(1, max_turns + 1):
    step = planner(state)
    trace.append({"turn": turn, "plan": step})

    if "final" in step:
        final_answer = step["final"]
        break

    result = TOOL_FUNCTIONS[step["tool"]](**step["args"])
    observation = {"tool": step["tool"], "args": step["args"], "result": result}
    state["observations"].append(observation)
    trace.append({"turn": turn, "observation": observation})
else:
    final_answer = {"allowed": None, "note": "No answer: max_turns reached."}

print("Question:", QUESTION)
for item in trace:
    print(item)
print("Final:", final_answer)
