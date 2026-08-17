# M1 · Model access quiz

## Multiple choice

1. What does it mean to treat a model as one function in an application?
   - A. Give it inputs, receive a probabilistic output, and design software around that boundary.
   - B. Assume it contains the complete business workflow.
   - C. Store all business rules inside the prompt.
   - D. Treat every response as deterministic.

   **Answer: A.** A model receives inputs and produces a probabilistic output.
   **Why:** The surrounding application must provide contracts, validation, and controls around that boundary.

2. Why is a model not a complete product?
   - A. A product also needs data boundaries, policy, user interaction, errors, and operations.
   - B. Models cannot be called from software.
   - C. Products do not need tests.
   - D. Models only produce numbers.

   **Answer: A.** A product also needs data boundaries, policy, user interaction, errors, and operations.
   **Why:** A model capability becomes useful only when integrated into a reliable workflow.

3. Which is the most important difference between a hosted and a local model
   access path?
   - A. Hosted access delegates infrastructure; local access keeps more control but requires more operations.
   - B. Hosted models are always more accurate.
   - C. Local models never use memory.
   - D. Hosted models cannot be monitored.

   **Answer: A.** Hosted access delegates infrastructure; local access keeps more control but requires more operations.
   **Why:** The deployment boundary changes who operates hardware and who controls the data path.

4. What is one reason an enterprise may prefer a governed platform boundary for
   model access?
   - A. Identity, policy, logging, and provider configuration can be managed consistently.
   - B. It guarantees that generated content is true.
   - C. It removes all usage cost.
   - D. It makes application code unnecessary.

   **Answer: A.** Identity, policy, logging, and provider configuration can be managed consistently.
   **Why:** Central governance makes access auditable and reduces duplicated provider-specific controls.

5. What should influence the choice between proprietary and open-weight models?
   - A. Required capability, privacy, license, latency, cost, and operating responsibility.
   - B. Brand popularity alone.
   - C. Parameter count alone.
   - D. Whether the prompt is short.

   **Answer: A.** Consider capability, privacy, license, latency, cost, and operating responsibility.
   **Why:** Model choice is an engineering and operating decision, not a brand preference.

6. Why is “choose the smallest sufficient model” a useful default?
   - A. It controls cost and latency while leaving room to increase capability when evidence requires it.
   - B. Smaller models never make mistakes.
   - C. It avoids evaluating quality.
   - D. It guarantees local deployment.

   **Answer: A.** It controls cost and latency while leaving room to increase capability when evidence requires it.
   **Why:** Start with measured sufficiency, then pay for more capability only when the requirement justifies it.

7. What should a provider-neutral model boundary usually hide?
   - A. Authentication, provider SDK details, response normalization, and provider errors.
   - B. The business requirement and all tests.
   - C. The user’s intended output.
   - D. Every application policy.

   **Answer: A.** It should hide authentication, provider SDK details, response normalization, and provider errors.
   **Why:** Features should depend on a stable application contract rather than a specific provider implementation.

8. Why is model output non-determinism an engineering concern?
   - A. Tests and downstream code need contracts, validation, and tolerance for variation.
   - B. It means models cannot be used in production.
   - C. It makes input validation unnecessary.
   - D. It only affects local models.

   **Answer: A.** Tests and downstream code need contracts, validation, and tolerance for variation.
   **Why:** Variable output must be made safe before another component relies on it.

9. Where should an API credential normally be loaded?
   - A. From protected runtime configuration, not hard-coded source or prompts.
   - B. From a public notebook output.
   - C. From the model’s generated answer.
   - D. From a user’s portfolio history.

   **Answer: A.** Load it from protected runtime configuration.
   **Why:** Secrets should not be embedded in source, prompts, notebooks, or participant-facing materials.

10. What is a safe application behavior when a model returns empty or unusable
    output?
    - A. Return a defined fallback or error, log the event, and avoid pretending the answer succeeded.
    - B. Retry forever.
    - C. Execute the requested action anyway.
    - D. Return the raw provider object to every caller.

    **Answer: A.** Return a defined fallback or error, log the event, and avoid pretending the answer succeeded.
    **Why:** A safe boundary prevents an empty or malformed result from becoming a false business success.

## Code reading and debugging

11. Why is this guard useful?

    ```python
    if api_key:
        response = call_model(api_key, prompt)
    else:
        response = "Model configuration is unavailable."
    ```

    **Answer:** The guard prevents an invalid provider call when configuration is missing.
    **Why:** It gives the caller a defined outcome instead of failing later with a confusing authentication error.

12. A provider SDK returns a response object with optional fields, while the
    application contract says `call_model(...) -> str`. What should the boundary
    do before returning?

    **Answer:** Extract and normalize the intended text, handle missing or empty fields, and return the documented string contract.
    **Why:** Downstream code should not depend on provider-specific response objects.

13. A local-model call fails because a model-loading option is passed to text
    generation. What is the likely issue, and how would you isolate it?

    **Answer:** A loading-only option was passed to the generation API. Reproduce the call with a tiny fixture, inspect the API boundary, and move the option to model loading.
    **Why:** Loading and generation have different supported parameters and failure modes.

## Scenario

14. An enterprise team wants to prototype an assistant offline, then deploy it
    behind a governed hosted service. Which parts of the application should stay
    stable while the model access path changes?

    **Expected answer:** Keep the application-level function signature, message/response contract, fallback behavior, logging, and tests stable; swap only the provider adapter/configuration.
    **Why:** A stable boundary allows infrastructure to change without rewriting business features.

## Capstone transfer

15. For a Chronos explanation assistant, specify the input/output contract of the
    model boundary and one policy for hallucinated, empty, or unsafe output.

    **Expected answer:** Accept role/content messages and return normalized text. Validate or review claims before action, and return a safe fallback when output is empty or violates policy.
    **Why:** Chronos needs a stable contract and a control point for untrusted model output.
