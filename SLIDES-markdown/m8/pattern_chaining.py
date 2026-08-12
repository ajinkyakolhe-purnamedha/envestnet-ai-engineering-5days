"""Advisor workflow, step 1: the chain.

The artifact M8.2 grows, slide by slide: gather ->
decide -> draft. Fully offline. Run:
    uv run python -m m8.pattern_chaining
"""

from chronos_offline import generate
from m8.advisor_tools import (check_guidelines,
                              get_current_price,
                              get_portfolio_allocation)


# #region pattern
facts = {
    "price": get_current_price("AAPL"),
    "allocation": get_portfolio_allocation(1),
    "check": check_guidelines("AAPL", 36.0),
}                                     # step 1: gather

verdict = ("blocked by the 35% limit"
           if not facts["check"]["allowed"]
           else "within guidelines")  # step 2: decide

note = generate(                      # step 3: draft
    f"Facts: {facts}. Verdict: {verdict}. "
    "Write a 2-sentence advisor note.")
# #endregion pattern

print("VERDICT:", verdict)
print("NOTE:", note)

# Python gathered the facts, Python decided the verdict,
# and only then did the model write prose. Compare
# M8.1.3: the autonomous agent got the answer WRONG
# because the planner controlled everything. Here the
# model cannot get the verdict wrong -- it never owned
# it. Same tiny model, reliable result: that is what
# choosing a workflow over an agent buys.
