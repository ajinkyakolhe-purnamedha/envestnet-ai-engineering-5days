"""Pattern 5: the smallest agentic loop.

Fully offline. Run:
    uv run --project ../CODE-ALONGS \
        python m3/pattern_agentic_loop.py
"""


def planner(goal: str, trace: list[str]) -> dict:
    if not trace:
        return {"tool": "lookup_policy", "args": "concentration"}
    return {"tool": "final", "args": "35% is the limit"}


def lookup_policy(topic: str) -> str:
    return f"{topic}: no holding may exceed 35%"


# #region pattern
TOOLS = {"lookup_policy": lookup_policy}


def run_agent(goal: str, max_steps: int = 3) -> list[str]:
    trace = []
    for _ in range(max_steps):
        plan = planner(goal, trace)
        if plan["tool"] == "final":
            trace.append("FINAL: " + plan["args"])
            return trace
        result = TOOLS[plan["tool"]](plan["args"])
        trace.append(f"{plan['tool']} -> {result}")
    trace.append("STOP: max_steps reached")
    return trace
# #endregion pattern


if __name__ == "__main__":
    print("\n".join(run_agent("Check the concentration policy.")))

# Pros: handles unknown step counts and dynamic tools.
# Cons: every step costs, and planner mistakes compound.
# A cap and trace are not optional; they are the runtime.
