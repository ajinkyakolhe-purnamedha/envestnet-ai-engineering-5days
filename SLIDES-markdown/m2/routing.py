"""Send the easy ones to the cheap model.

Run:
    uv run --project ../CODE-ALONGS \
        python m2/routing.py
"""

from chronos_offline import embed, similarity

SIMPLE = "look up one stored value: a price or a balance"
HARD = "multi-step reasoning, planning, tax analysis"

simple_v, hard_v = embed([SIMPLE, HARD])


# #region route
def is_simple(question: str) -> bool:
    q = embed([question])[0]
    return similarity(q, simple_v) > similarity(q, hard_v)


def answer(question: str) -> str:
    if is_simple(question):
        return f"[local model] {question}"
    return f"[frontier model] {question}"
# #endregion route


for q in [
    "What is AAPL's close on 2020-06-01?",
    "How many shares of MSFT does Bob hold?",
    "Model the tax impact of rebalancing Alice's book.",
    "Compare three rebalancing strategies and recommend one.",
]:
    print(f"{'SIMPLE' if is_simple(q) else 'HARD':>6}  {q}")

# Lesson: route by meaning before you spend model tokens.
# But measure accuracy; one wrong route can cost two calls.
