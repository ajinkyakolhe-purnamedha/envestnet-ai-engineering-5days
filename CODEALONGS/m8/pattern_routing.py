"""Advisor workflow, step 2: a front door.

Same workflow as pattern_chaining -- routing decides
which questions ever reach it. Fully offline. Run:
    uv run --project ../CODE-ALONGS \
        python m8/pattern_routing.py
"""

import sys

from chronos_offline import embed, similarity


# #region pattern
ROUTES = {
    "price":  ["What is AAPL trading at?",
               "How much does one share cost now?"],
    "policy": ["What does our policy document say?",
               "What are the rules about cash limits?"],
    "trade":  ["Buy 100 shares of AAPL now.",
               "Sell all my holdings today."],
}


def route(question: str) -> str:
    q = embed([question])[0]
    scores = {label: max(similarity(q, embed([ex])[0])
                         for ex in examples)
              for label, examples in ROUTES.items()}
    return max(scores, key=scores.get)
# #endregion pattern


def show_scores(question: str) -> None:
    """Print every route's score -- the router's reasoning."""
    q = embed([question])[0]
    for label, examples in ROUTES.items():
        best = max(similarity(q, embed([ex])[0])
                   for ex in examples)
        print(f"  {label:6}  {best:.3f}")
    print("-> routed to:", route(question))


if __name__ == "__main__":
    # Pass your own question to see the scores:
    #   uv run --project ../CODE-ALONGS \
    #       python m8/pattern_routing.py "..."
    if len(sys.argv) > 1:
        show_scores(" ".join(sys.argv[1:]))
        raise SystemExit(0)
    for q in ["How expensive is MSFT right now?",
              "Is 40% cash within our guidelines?",
              "Please sell everything today."]:
        label = route(q)
        action = ("REFUSED, no tool touched"
                  if label == "trade"
                  else "-> run the advisor workflow")
        print(f"{label:6}  {action:30}  {q}")

# Routing on embeddings, not on chat: the M2 lesson
# applied. SmolLM2 cannot follow "answer with one word",
# but the BGE embeddings separate these intents cleanly.
#
# Found by testing: ONE example per route misrouted
# "How expensive is MSFT right now?" to policy. Two or
# three examples per intent fixed every test case. Cheap
# lesson: routes are defined by examples, so give each
# route enough of them to cover its phrasings.
#
# And note the governance move -- "trade" is a route so
# that trade-like requests are RECOGNIZED and refused by
# Python. No trade tool exists to call, same rule as M7.
