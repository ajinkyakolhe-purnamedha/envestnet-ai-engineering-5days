# M0 · Python Foundations quiz

Answer without running the code unless a question explicitly asks you to reason about it.

## Multiple choice

1. Why is Python widely used in AI engineering?
   - A. It is the only language that can call a model.
   - B. It combines readable application code with a large data and model ecosystem.
   - C. It guarantees every model runs locally.
   - D. It removes the need for tests.

2. Which statement best separates an AI engineer from an AI researcher?
   - A. The engineer integrates reliable capabilities into useful systems; the researcher develops or studies model capabilities.
   - B. The engineer never uses mathematics.
   - C. The researcher only writes web servers.
   - D. There is no practical difference.

3. In the course ecosystem, which item is primarily a model provider?
   - A. SQLite
   - B. FastAPI
   - C. Google Gemini
   - D. pytest

4. What is the main purpose of a virtual environment or project dependency file?
   - A. To make a model more intelligent
   - B. To make the project’s package requirements reproducible
   - C. To encrypt API keys
   - D. To replace source control

5. What should an application do before making a hosted model call?
   - A. Hard-code the API key in the Python file.
   - B. Load configuration from a controlled environment and handle missing configuration.
   - C. Delete the user’s history.
   - D. Disable logging.

6. What does a type hint such as `shares: int` primarily provide?
   - A. Runtime enforcement in every Python program
   - B. A readable contract for tools, reviewers, and maintainers
   - C. Automatic database storage
   - D. Model fine-tuning

7. Why put repeated logic in a function?
   - A. To make it harder to test
   - B. To give the behavior a named, reusable, testable boundary
   - C. To avoid all error handling
   - D. To turn Python into Java

8. What is SQLite useful for in the wealth demo?
   - A. Persisting small structured application data without a separate database server
   - B. Generating model weights
   - C. Replacing an HTTP API
   - D. Rendering notebooks

9. What is the purpose of a FastAPI health endpoint?
   - A. To prove the model is factually correct
   - B. To provide a simple operational check that the service is reachable
   - C. To calculate portfolio returns
   - D. To store secrets

10. Which practice makes a small application easier to operate?
   - A. Print arbitrary values everywhere.
   - B. Combine logging, tests, and deliberate debugging points.
   - C. Catch every exception and ignore it.
   - D. Keep all logic in one giant function.

## Code reading and debugging

11. Given:

    ```python
    def purchase_cost(shares: int, price: float) -> float:
        if shares <= 0 or price <= 0:
            raise ValueError("Shares and price must be positive.")
        return shares * price
    ```

    What happens for `purchase_cost(10, 80.50)` and for `purchase_cost(0, 80.50)`?

12. A server imports `wealth_demo.models`, but the command is run from the
    repository root and fails with `ModuleNotFoundError`. What is the most
    direct diagnosis?

    - A. The model class is invalid.
    - B. The package is not on Python’s import path for that launch location.
    - C. SQLite cannot be imported.
    - D. FastAPI requires a model key.

13. This code is intended to read an API key:

    ```python
    key = os.getenv("GEMINI_KEY")
    if key:
        call_model(key)
    ```

    The documented environment variable is `GEMINI_API_KEY`. What is wrong?

## Scenario

14. In the M0 wealth-demo lab, a learner can calculate a purchase cost but the
    result is not persisted and cannot be inspected through the service. What
    small sequence of boundaries should they add next: model, storage, server,
    or all three at once? Explain the order.

## Capstone transfer

15. Chronos needs to expose a portfolio summary endpoint. Name one reusable
    Python function boundary, one validation rule, and one test you would add
    before connecting the endpoint to a model.
