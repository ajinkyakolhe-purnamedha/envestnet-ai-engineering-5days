# M1 · Model access quiz

## Multiple choice

1. What does it mean to treat a model as one function in an application?
   - A. Treat every response as deterministic.
   - B. Give it inputs, receive a probabilistic output, and design software around that boundary.
   - C. Store all business rules inside the prompt.
   - D. Assume it contains the complete business workflow.

2. Why is a model not a complete product?
   - A. Models only produce numbers.
   - B. Models cannot be called from software.
   - C. A product also needs data boundaries, policy, user interaction, errors, and operations.
   - D. Products do not need tests.

3. Which is the most important difference between a hosted and a local model
   access path?
   - A. Hosted models cannot be monitored.
   - B. Hosted models are always more accurate.
   - C. Local models never use memory.
   - D. Hosted access delegates infrastructure; local access keeps more control but requires more operations.

4. What is one reason an enterprise may prefer a governed platform boundary for
   model access?
   - A. Identity, policy, logging, and provider configuration can be managed consistently.
   - B. It makes application code unnecessary.
   - C. It guarantees that generated content is true.
   - D. It removes all usage cost.

5. What should influence the choice between proprietary and open-weight models?
   - A. Parameter count alone.
   - B. Required capability, privacy, license, latency, cost, and operating responsibility.
   - C. Whether the prompt is short.
   - D. Brand popularity alone.

6. Why is “choose the smallest sufficient model” a useful default?
   - A. It guarantees local deployment.
   - B. Smaller models never make mistakes.
   - C. It controls cost and latency while leaving room to increase capability when evidence requires it.
   - D. It avoids evaluating quality.

7. What should a provider-neutral model boundary usually hide?
   - A. The user’s intended output.
   - B. The business requirement and all tests.
   - C. Every application policy.
   - D. Authentication, provider SDK details, response normalization, and provider errors.

8. Why is model output non-determinism an engineering concern?
   - A. It makes input validation unnecessary.
   - B. It only affects local models.
   - C. It means models cannot be used in production.
   - D. Tests and downstream code need contracts, validation, and tolerance for variation.

9. Where should an API credential normally be loaded?
   - A. From the model’s generated answer.
   - B. From protected runtime configuration, not hard-coded source or prompts.
   - C. From a user’s portfolio history.
   - D. From a public notebook output.

10. What is a safe application behavior when a model returns empty or unusable
    output?
    - A. Execute the requested action anyway.
    - B. Return the raw provider object to every caller.
    - C. Return a defined fallback or error, log the event, and avoid pretending the answer succeeded.
    - D. Retry forever.

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
