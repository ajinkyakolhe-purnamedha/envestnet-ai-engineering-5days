"""Pattern 4: orchestrator-workers. Plan, delegate, write.

Fully offline. Run:
    uv run --project ../CODE-ALONGS \
        python m8/pattern_orchestrator.py
"""

from chronos_offline import generate
from m8.advisor_tools import (get_current_price,
                              get_portfolio_allocation)


# #region pattern
def research_worker(symbol: str) -> dict:
    return {"symbol": symbol,
            "price": get_current_price(symbol),
            "alloc": get_portfolio_allocation(1)}


def orchestrator(question: str) -> str:
    symbols = [s for s in ["AAPL", "MSFT", "GLD"]
               if s in question]          # plan
    findings = [research_worker(s)
                for s in symbols]         # delegate
    return generate(                      # synthesize
        f"Findings: {findings}. Draft the "
        "advisor summary in 2 sentences.")
# #endregion pattern


if __name__ == "__main__":
    print(orchestrator("Compare AAPL and GLD for Alice."))

# Plan, delegate, synthesize. Here the planning rule is
# deterministic (symbols named in the question); with a
# frontier model, that step becomes a model call that
# returns a work list -- the shape of every "deep
# research" product, and of Lab 8's four-role advisor
# report. The workers stay dumb on purpose: workers
# execute, the orchestrator decides.
