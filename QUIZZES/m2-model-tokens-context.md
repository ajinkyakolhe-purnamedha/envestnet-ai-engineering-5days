# M2 · Model, tokens, and context quiz

## Multiple choice

1. What is a token?
   - A. A small piece of text used by a model
   - B. A user password
   - C. A database server
   - D. A Python package

2. What is a context window?
   - A. The maximum amount of request context a model can process
   - B. The size of a user interface
   - C. The number of model providers
   - D. The time needed to install Python

3. What is usually included in a model request?
   - A. Instructions, history, the current input, and any supplied context
   - B. Only the last word
   - C. Only the output
   - D. Only the API key

4. Why does an application often send conversation history again?
   - A. The application keeps the state and sends the relevant parts to a stateless call.
   - B. The model permanently remembers every user.
   - C. History is part of the Python interpreter.
   - D. The server automatically stores every prompt.

5. Why count tokens?
   - A. To estimate context use, cost, and possible limits
   - B. To improve spelling only
   - C. To replace testing
   - D. To change the model’s training data

6. What should happen when a request is too large?
   - A. Apply a clear policy such as trimming, summarizing, retrieving, or rejecting.
   - B. Ignore the limit.
   - C. Delete all instructions.
   - D. Keep retrying forever.

7. Why can trimming history be dangerous?
   - A. It may remove information or break the expected message order.
   - B. It always makes responses longer.
   - C. It changes Python types.
   - D. It creates a new model.

8. What does input usage measure?
   - A. How much request text was processed
   - B. How many users signed in
   - C. How many database rows exist
   - D. How many Python files exist

9. Why measure latency and cost as well as output quality?
   - A. A useful system must meet quality and operational constraints together.
   - B. Quality never matters.
   - C. Cost determines truth.
   - D. Latency is unrelated to users.

10. What is an embedding commonly used for?
    - A. Comparing the meaning of text
    - B. Storing an API key
    - C. Running a web server
    - D. Validating every business rule

## Code reading and debugging

11. What does this code keep?

    ```python
    recent = messages[-4:]
    ```

12. Why is this estimate incomplete?

    ```python
    cost = output_tokens * output_rate
    ```

13. A trimmed message list begins with an assistant message. Why might that be
    a problem, and what simple correction can be made?

## Scenario

14. A chat application becomes slower and more expensive as the conversation
    grows. What two measurements would you collect first, and what simple policy
    could you try?

## Capstone transfer

15. Give one rule for keeping a Chronos assistant within its context budget.
