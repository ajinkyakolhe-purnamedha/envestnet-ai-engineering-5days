"""YOU implement: the front door (routing pattern, M8.2.3).

Decide what kind of question this is BEFORE any tool runs. A keyword
router is enough — deterministic and testable. It must recognize
sell-shaped phrasings (sell, liquidate, cash out, dump, ...) so the
workflow can refuse them: advisors never execute trades.
"""

PORTFOLIO_ROUTE = "portfolio"
POLICY_ROUTE = "policy"
TRADE_ROUTE = "trade"


def route_client_question(question: str) -> str:
    """Return one of the three route constants above.

    Hints:
    - lowercase the question once
    - trade words win over policy words (refusing is the safest branch)
    - anything unrecognized is a portfolio question
    """
    raise NotImplementedError("M8 lab step 1: write the keyword router")
