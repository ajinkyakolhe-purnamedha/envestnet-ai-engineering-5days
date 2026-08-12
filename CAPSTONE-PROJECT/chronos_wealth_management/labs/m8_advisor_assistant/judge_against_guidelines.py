"""YOU implement: the verdict (chaining pattern step 2, M8.2.2).

Python owns this decision. The model never sees it undecided — that is
how the morning's workflow fixed the honest trace.
"""

from chronos.advisor_workspace.analyze_client_portfolio import (
    CONCENTRATION_THRESHOLD,
    HIGH_CASH_THRESHOLD,
)
from chronos.shared_database.api_schemas import AdvisorMetricResponse


def judge_against_guidelines(metrics: AdvisorMetricResponse) -> str:
    """Return "within guidelines", or a string starting with
    "outside guidelines: " that names every breach.

    Hints:
    - reuse the two imported thresholds — do NOT restate 0.35
    - a concentration breach must mention the 35% concentration limit
    - a cash breach must mention the 40% guideline
    - metrics.largest_position_ratio and metrics.cash_ratio are floats
    """
    raise NotImplementedError("M8 lab step 3: write the verdict")
