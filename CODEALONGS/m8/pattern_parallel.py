"""Advisor workflow, step 3: parallelize the gather.

Same workflow as pattern_chaining -- step 1 fans out.
Fully offline. Run:
    uv run --project ../CODE-ALONGS \
        python m8/pattern_parallel.py
"""

from m8.advisor_tools import (check_guidelines,
                              get_current_price,
                              get_portfolio_allocation)


# #region pattern
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as pool:
    price = pool.submit(get_current_price, "AAPL")
    alloc = pool.submit(get_portfolio_allocation, 1)
    check = pool.submit(check_guidelines, "AAPL", 36.0)

facts = {"price": price.result(),
         "allocation": alloc.result(),
         "check": check.result()}
# #endregion pattern

print("FACTS:", facts)

# This is pattern_chaining's step 1, fanned out: the
# three lookups are independent, so they run at once and
# the workflow's decide + draft steps are unchanged.
# Parallel tool calls are a parallelism feature, not an
# intelligence feature -- ThreadPoolExecutor is Python
# you knew before this workshop, and it is what ships
# underneath when a framework advertises the same thing.
# (Gemini did it unprompted in M8.3.2: three tool calls
# in one model response.)
