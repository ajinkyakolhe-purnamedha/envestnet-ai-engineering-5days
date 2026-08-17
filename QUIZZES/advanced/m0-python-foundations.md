# M0 · Python Foundations — advanced quiz

## Multiple choice

1. A calculation is correct but is duplicated in an API handler, notebook, and
   batch script. What is the most important engineering risk?
   - A. Behavioral drift when one copy changes and the others do not
   - B. Python will stop accepting floats
   - C. SQLite will delete the data
   - D. The model will become non-deterministic

2. A team’s code works locally but fails in CI because a package version changed.
   Which improvement addresses the root cause?
   - A. Declare and lock dependencies in a reproducible project environment
   - B. Add more print statements
   - C. Catch every exception
   - D. Move the package import into a class

3. Where should validation occur if both an HTTP endpoint and a scheduled job
   can create the same holding?
   - A. In a shared domain/application boundary used by both callers
   - B. Only in the HTTP handler
   - C. Only in the database UI
   - D. Only in a notebook

4. Which design best separates a portfolio calculation from persistence?
   - A. A pure calculation function called by storage/application code
   - B. SQL embedded in every arithmetic expression
   - C. A global database connection inside the calculation
   - D. A model call that decides the arithmetic

5. An endpoint returns HTTP 200 with an error string when input is invalid. Why
   is this a weak contract?
   - A. Clients cannot reliably distinguish a successful response from a failure
   - B. HTTP cannot return JSON
   - C. Validation should happen after persistence
   - D. Error strings are always unsafe

6. Which test boundary gives the fastest feedback for an invalid purchase rule?
   - A. A unit test of the validation/calculation function
   - B. A full browser test against a deployed service
   - C. A model-quality evaluation
   - D. A log review after release

7. A local SQLite database is adequate for a classroom service but not necessarily
   for a multi-instance production service. What changed?
   - A. The persistence and concurrency requirements changed
   - B. Python functions stopped working
   - C. Type hints became invalid
   - D. HTTP no longer has contracts

8. Which log entry is most useful for diagnosing a failed request without leaking
   secrets?
   - A. Request ID, operation, outcome, duration, and error category
   - B. Full API key and raw user credentials
   - C. Only the word “failed”
   - D. The entire environment file

9. A package imports successfully in an IDE but not in a shell. Which explanation
   is most plausible?
   - A. The IDE and shell use different interpreters, working directories, or environments
   - B. Classes only work in IDEs
   - C. SQLite changes Python imports
   - D. Logging disables imports

10. What is the best reason to keep deterministic business calculations outside
    an LLM call?
    - A. They need repeatable, testable results and explicit error handling
    - B. LLMs cannot read numbers
    - C. Python cannot call models
    - D. Databases cannot store model output

## Code reading and debugging

11. What bug remains in this function even though its type hints look reasonable?

    ```python
    def price_change(old: float, new: float) -> float:
        return new - old
    ```

    State one validation or domain rule that may be required.

12. A test mutates a returned list and a later test unexpectedly sees the same
    item. What kind of design issue should you investigate?

13. A service’s unit tests pass, but its endpoint returns stale data after a
    restart. Which boundary is most likely untested?

## Scenario

14. Design a small purchase workflow with calculation, validation, persistence,
    and HTTP layers. Identify one invariant that must hold across all layers and
    one failure that should never be silently converted into success.

## Capstone transfer

15. For Chronos, define a deterministic “portfolio summary” contract that an AI
    assistant may consume, including one freshness or data-integrity check.
