"""Advisor workflow, step 4: gate the draft.

Same workflow -- the chain's draft now faces a critic.
Fully offline. Run:
    uv run --project ../CODE-ALONGS \
        python m8/pattern_evaluator.py
"""

from chronos_offline import generate
from m8.advisor_tools import (check_guidelines,
                              get_current_price,
                              get_portfolio_allocation)

facts = {                      # the chain's step 1
    "price": get_current_price("AAPL"),
    "allocation": get_portfolio_allocation(1),
    "check": check_guidelines("AAPL", 36.0),
}


# #region pattern
draft = generate("Write a 2-sentence advisor note "
                 f"from: {facts}")

problems = []
if "35" not in draft:
    problems.append("must cite the 35% limit")
if len(draft.split()) > 60:
    problems.append("too long")

if problems:
    draft = generate(f"Rewrite: {draft}. "
                     f"Fix: {problems}")
# #endregion pattern

print("PROBLEMS:", problems or "none")
print("FINAL:", draft)

# The evaluator is deterministic Python -- rules you can
# assert, not model vibes. The cheapest quality gate is
# an if-statement; LLM-as-judge (M13) comes only after
# rules run out. And the loop is bounded to ONE revision:
# evaluator loops need a max_turns exactly like agent
# loops, or a stubborn draft spins forever.
