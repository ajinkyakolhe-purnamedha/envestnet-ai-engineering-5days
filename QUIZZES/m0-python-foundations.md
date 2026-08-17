# M0 · Python Foundations quiz

## Multiple choice

1. Why is Python a strong default for AI application engineering?
   - A. It combines readable application code with mature data, web, and model libraries.
   - B. It guarantees every model is accurate.
   - C. It removes the need for environment management.
   - D. It can only be used for prototypes.

2. Why should a project declare its dependencies instead of relying on whatever
   packages happen to be installed globally?
   - A. To make setup and execution reproducible for another developer or deployment.
   - B. To make the model produce longer answers.
   - C. To prevent all runtime errors.
   - D. To avoid using source control.

3. Where should a rule such as “shares and price must be positive” be enforced?
   - A. At the application boundary before invalid data is persisted or acted on.
   - B. Only in a presentation slide.
   - C. Only after a model has responded.
   - D. Nowhere if the caller is trusted.

4. What is the main benefit of putting repeated behavior in a function?
   - A. It creates a named unit that can be reused and tested independently.
   - B. It makes the behavior impossible to change.
   - C. It automatically stores results in a database.
   - D. It removes the need for inputs.

5. When is a class a useful choice in a small application?
   - A. When related state and operations need a clear, reusable boundary.
   - B. Whenever a single expression is used once.
   - C. Only when calling a hosted model.
   - D. When logging should be avoided.

6. Why might a small wealth application use SQLite rather than an in-memory list?
   - A. It needs data to survive process restarts and be queried consistently.
   - B. SQLite automatically validates every business rule.
   - C. SQLite is a model provider.
   - D. In-memory data cannot be tested.

7. What should an HTTP endpoint expose as part of its contract?
   - A. Expected inputs, response shape, and meaningful error behavior.
   - B. The implementation’s local variable names only.
   - C. The developer’s API key.
   - D. Every internal database table.

8. Which test gives the strongest feedback about a pure calculation function?
   - A. A deterministic unit test with representative valid and invalid inputs.
   - B. A screenshot of the source code.
   - C. A production log search only.
   - D. A test that never asserts a result.

9. What is the operational value of structured logging?
   - A. It makes important events and failures searchable across executions.
   - B. It replaces validation and tests.
   - C. It guarantees the service is available.
   - D. It hides implementation errors from operators.

10. A program works from one directory but cannot import its package from another.
    What should be checked first?
    - A. The project layout, launch command, and Python import path.
    - B. The model’s parameter count.
    - C. The database’s market data.
    - D. The user interface color.

## Code reading and debugging

11. What is the observable behavior of this function for `shares=0` and for
    `shares=10, price=80.5`?

    ```python
    def purchase_cost(shares: int, price: float) -> float:
        if shares <= 0 or price <= 0:
            raise ValueError("Shares and price must be positive.")
        return shares * price
    ```

12. A test expects `purchase_cost(10, 80.5) == 805`, but the implementation
    returns a string such as `"805.0"`. What contract has been broken, and where
    should it be fixed?

13. A service passes validation in a notebook but fails when started through the
    documented server command. Name two environment or launch differences worth
    checking before changing the application logic.

## Scenario

14. A small portfolio service must accept a purchase, reject invalid values,
    save valid data, and expose it over HTTP. Describe a sensible implementation
    order and one test for each boundary.

## Capstone transfer

15. For a Chronos portfolio-summary feature, define one Python function boundary,
    its input/output contract, and one failure case that must be tested before
    connecting it to an AI assistant.
