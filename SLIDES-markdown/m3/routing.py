"""Three tiers, one router. Model choice is economics.

Fully offline. Run:
    uv run --project ../CODE-ALONGS \
        python m3/routing.py
"""

from chronos_offline import embed, similarity

TIERS = {"fast": "$0.15", "default": "$1.00", "deep": "$15.00"}

PROTOTYPES = {
    "fast": "extract a field, classify, look up one value",
    "default": "summarise a portfolio, write a client update",
    "deep": "plan a multi-step strategy, weigh trade-offs",
}

# #region route
_names = list(PROTOTYPES)
_vectors = embed([PROTOTYPES[n] for n in _names])

def pick_tier(question: str) -> str:
    q = embed([question])[0]
    scores = [similarity(q, v) for v in _vectors]
    return _names[scores.index(max(scores))]


def answer(question: str) -> str:
    tier = pick_tier(question)
    return f"[{tier} tier, {TIERS[tier]}/1M] {question}"
# #endregion route

if __name__ == "__main__":
    for q in [
        "Extract the symbol from this advisor note.",
        "Summarise Alice's portfolio for her quarterly review.",
        "Plan a rebalance that respects the 35% limit.",
    ]:
        print(f"{pick_tier(q):>7}  {q}")

# Lesson: model choice is an economic decision. Use the
# cheapest tier that is still good enough for the task.
