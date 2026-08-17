# M1 · Model access — advanced quiz

## Multiple choice

1. A model is highly capable but produces variable output. Which design most
   directly makes it usable by a business workflow?
   - A. A typed/validated boundary with explicit fallback and observability
   - B. A longer prompt with no tests
   - C. More model parameters only
   - D. Removing all user context

   **Answer: A.** Use a typed/validated boundary with fallback and observability.
   **Why:** The workflow needs a stable contract around variable model output.

2. A regulated team needs provider flexibility and auditable access. Which
   boundary is most appropriate?
   - A. Application code calls one internal interface while adapters handle providers and policy
   - B. Every feature calls a provider SDK directly
   - C. Users paste keys into prompts
   - D. A model chooses which provider to use without logging

   **Answer: A.** Use one internal interface with provider adapters and policy.
   **Why:** This centralizes governance while preserving provider flexibility.

3. A local model reduces data egress but increases deployment complexity. What
   decision principle follows?
   - A. Compare privacy/control gains against hardware, reliability, and maintenance costs
   - B. Local is always the enterprise default
   - C. Hosted is always prohibited
   - D. Accuracy no longer matters

   **Answer: A.** Compare privacy/control gains against hardware, reliability, and maintenance costs.
   **Why:** Local inference changes the operating burden; it does not remove quality requirements.

4. What is the strongest reason to evaluate a smaller model before a larger one?
   - A. It establishes whether the requirement can meet quality, latency, and cost targets with less operational burden.
   - B. Smaller models never hallucinate.
   - C. It avoids writing an evaluation.
   - D. It guarantees the same output.

   **Answer: A.** Evaluate whether the smaller model meets quality, latency, and cost targets.
   **Why:** Evidence should justify additional capability and cost.

5. Which concern belongs in a model adapter rather than in every business feature?
   - A. Provider response normalization and provider-specific retry/error mapping
   - B. The portfolio allocation policy
   - C. The user’s business goal
   - D. The acceptance test for a trade

   **Answer: A.** Provider response normalization and provider-specific retry/error mapping.
   **Why:** Provider mechanics belong in adapters, not duplicated in business features.

6. A provider outage occurs. Which fallback is safest for an explanation feature?
   - A. Return a clear unavailable response and preserve the request for controlled retry or review.
   - B. Invent a likely explanation from memory.
   - C. Execute the next business action anyway.
   - D. Expose the provider exception and API key.

   **Answer: A.** Return a clear unavailable response and preserve the request for controlled retry or review.
   **Why:** An outage must not become an invented explanation or uncontrolled action.

7. Which combination best describes open-weight model selection?
   - A. Family capability/license, parameter size, hardware fit, and serving responsibility
   - B. Brand name and prompt length only
   - C. API price only
   - D. Context window only

   **Answer: A.** Consider family capability/license, parameter size, hardware fit, and serving responsibility.
   **Why:** Open-model selection includes both model properties and operating obligations.

8. Why is “model access” only the first engineering problem?
   - A. Reliability, data grounding, evaluation, security, and user workflow still surround the call.
   - B. Models cannot be integrated into applications.
   - C. Access automatically solves governance.
   - D. The first call is always production-ready.

   **Answer: A.** Reliability, grounding, evaluation, security, and workflow still surround the call.
   **Why:** Access is only one layer of an AI application.

9. What should a model boundary do with malformed provider output?
   - A. Normalize or reject it according to a documented contract and emit useful telemetry.
   - B. Pass it to every downstream component unchanged.
   - C. Silently convert it to a successful action.
   - D. Delete the request.

   **Answer: A.** Normalize or reject malformed output under a documented contract and emit telemetry.
   **Why:** Downstream components need a safe, observable boundary.

10. A team optimizes only model quality and ignores latency and cost. What is the
    likely enterprise consequence?
    - A. A technically strong feature may fail its service or budget constraints.
    - B. The model will become deterministic.
    - C. Privacy risk disappears.
    - D. Tests become unnecessary.

    **Answer: A.** A strong feature may still fail service-level or budget constraints.
    **Why:** Enterprise quality includes operational viability, not output quality alone.

## Code reading and debugging

11. Why is this return contract safer than returning the raw provider object?

    ```python
    def call_model(messages: list[dict[str, str]]) -> str:
        response = provider.generate(messages)
        return response.text or ""
    ```

    **Answer:** It returns a stable string contract and converts empty text into an explicit empty value.
    **Why:** Callers do not need to understand provider-specific response objects.

12. A retry wrapper retries every exception three times, including invalid input
    and authentication failure. What is wrong with that policy?

    **Answer:** It retries non-transient failures.
    **Why:** Invalid input and authentication errors will not be fixed by retrying; classify errors and retry only bounded transient failures.

13. A local model and a hosted model produce different output shapes for the same
    task. Where should compatibility logic live?

    **Answer:** In the provider adapter or normalization layer.
    **Why:** Business features should consume one stable contract rather than duplicate conversions.

## Scenario

14. Choose between hosted and local inference for an internal assistant that
    handles sensitive data, has a small pilot load, and needs centralized audit
    logs. State the trade-off and what evidence would change your decision.

    **Expected answer:** Local improves data control but adds operations; hosted can simplify operations and centralized audit but requires governance over data egress. Use evidence about data classification, audit, latency, cost, and operating capacity.
    **Why:** The choice is a measurable enterprise trade-off, not a universal rule.

## Capstone transfer

15. Specify Chronos’s provider-neutral model boundary, including its inputs,
    normalized output, timeout behavior, and one audit field.

    **Expected answer:** For example, `call_model(messages, request_id) -> str`; timeout returns a controlled unavailable result; log request ID, model/deployment, latency, usage, and outcome without secrets.
    **Why:** Chronos needs a stable feature contract, bounded failure behavior, and reconstructable telemetry.
