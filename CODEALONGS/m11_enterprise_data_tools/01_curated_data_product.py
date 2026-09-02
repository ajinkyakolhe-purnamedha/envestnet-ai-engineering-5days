"""One concept: simple services expose bounded business facts.

Try:
- Change max_positions from 2 to 4.
- Compare a portfolio snapshot with an advisor review report.
- Explain why a model should not calculate concentration percentages.
"""

from governed_data_product import build_current_portfolio_snapshot, generate_advisor_review_report


print("Portfolio snapshot:", build_current_portfolio_snapshot("alice", max_positions=2))
print("Advisor review report:", generate_advisor_review_report("alice"))
try:
    build_current_portfolio_snapshot("alice", max_positions=4)
except ValueError as error:
    print("Rejected before the read model:", error)
