# M1 · Model access quiz

## Multiple choice

1. What does it mean to treat a model as one function in an application?
   - A. Give it inputs, receive a probabilistic output, and design software around that boundary.
   - B. Assume it contains the complete business workflow.
   - C. Store all business rules inside the prompt.
   - D. Treat every response as deterministic.

2. Why is a model not a complete product?
   - A. A product also needs data boundaries, policy, user interaction, errors, and operations.
   - B. Models cannot be called from software.
   - C. Products do not need tests.
   - D. Models only produce numbers.

3. Which is the most important difference between a hosted and a local model
   access path?
   - A. Hosted access delegates infrastructure; local access keeps more control but requires more operations.
   - B. Hosted models are always more accurate.
   - C. Local models never use memory.
   - D. Hosted models cannot be monitored.

4. What is one reason an enterprise may prefer a governed platform boundary for
   model access?
   - A. Identity, policy, logging, and provider configuration can be managed consistently.
   - B. It guarantees that generated content is true.
   - C. It removes all usage cost.
   - D. It makes application code unnecessary.

5. What should influence the choice between proprietary and open-weight models?
   - A. Required capability, privacy, license, latency, cost, and operating responsibility.
   - B. Brand popularity alone.
   - C. Parameter count alone.
   - D. Whether the prompt is short.

6. Why is “choose the smallest sufficient model” a useful default?
   - A. It controls cost and latency while leaving room to increase capability when evidence requires it.
   - B. Smaller models never make mistakes.
   - C. It avoids evaluating quality.
   - D. It guarantees local deployment.

7. What should a provider-neutral model boundary usually hide?
   - A. Authentication, provider SDK details, response normalization, and provider errors.
   - B. The business requirement and all tests.
   - C. The user’s intended output.
   - D. Every application policy.

8. Why is model output non-determinism an engineering concern?
   - A. Tests and downstream code need contracts, validation, and tolerance for variation.
   - B. It means models cannot be used in production.
   - C. It makes input validation unnecessary.
   - D. It only affects local models.

9. Where should an API credential normally be loaded?
   - A. From protected runtime configuration, not hard-coded source or prompts.
   - B. From a public notebook output.
   - C. From the model’s generated answer.
   - D. From a user’s portfolio history.

10. What is a safe application behavior when a model returns empty or unusable
    output?
    - A. Return a defined fallback or error, log the event, and avoid pretending the answer succeeded.
    - B. Retry forever.
    - C. Execute the requested action anyway.
    - D. Return the raw provider object to every caller.

## Code reading and debugging

11. Why is this guard useful?

    ```python
    if api_key:
        response = call_model(api_key, prompt)
    else:
        response = "Model configuration is unavailable."
    ```

12. A provider SDK returns a response object with optional fields, while the
    application contract says `call_model(...) -> str`. What should the boundary
    do before returning?

13. A local-model call fails because a model-loading option is passed to text
    generation. What is the likely issue, and how would you isolate it?

## Scenario

14. An enterprise team wants to prototype an assistant offline, then deploy it
    behind a governed hosted service. Which parts of the application should stay
    stable while the model access path changes?

## Capstone transfer

15. For a Chronos explanation assistant, specify the input/output contract of the
    model boundary and one policy for hallucinated, empty, or unsafe output.
