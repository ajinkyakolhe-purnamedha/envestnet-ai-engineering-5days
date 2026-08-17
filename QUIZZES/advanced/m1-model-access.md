# M1 · Model access — advanced quiz

## Multiple choice

1. A model is highly capable but produces variable output. Which design most
   directly makes it usable by a business workflow?
   - A. A typed/validated boundary with explicit fallback and observability
   - B. A longer prompt with no tests
   - C. More model parameters only
   - D. Removing all user context

2. A regulated team needs provider flexibility and auditable access. Which
   boundary is most appropriate?
   - A. Application code calls one internal interface while adapters handle providers and policy
   - B. Every feature calls a provider SDK directly
   - C. Users paste keys into prompts
   - D. A model chooses which provider to use without logging

3. A local model reduces data egress but increases deployment complexity. What
   decision principle follows?
   - A. Compare privacy/control gains against hardware, reliability, and maintenance costs
   - B. Local is always the enterprise default
   - C. Hosted is always prohibited
   - D. Accuracy no longer matters

4. What is the strongest reason to evaluate a smaller model before a larger one?
   - A. It establishes whether the requirement can meet quality, latency, and cost targets with less operational burden.
   - B. Smaller models never hallucinate.
   - C. It avoids writing an evaluation.
   - D. It guarantees the same output.

5. Which concern belongs in a model adapter rather than in every business feature?
   - A. Provider response normalization and provider-specific retry/error mapping
   - B. The portfolio allocation policy
   - C. The user’s business goal
   - D. The acceptance test for a trade

6. A provider outage occurs. Which fallback is safest for an explanation feature?
   - A. Return a clear unavailable response and preserve the request for controlled retry or review.
   - B. Invent a likely explanation from memory.
   - C. Execute the next business action anyway.
   - D. Expose the provider exception and API key.

7. Which combination best describes open-weight model selection?
   - A. Family capability/license, parameter size, hardware fit, and serving responsibility
   - B. Brand name and prompt length only
   - C. API price only
   - D. Context window only

8. Why is “model access” only the first engineering problem?
   - A. Reliability, data grounding, evaluation, security, and user workflow still surround the call.
   - B. Models cannot be integrated into applications.
   - C. Access automatically solves governance.
   - D. The first call is always production-ready.

9. What should a model boundary do with malformed provider output?
   - A. Normalize or reject it according to a documented contract and emit useful telemetry.
   - B. Pass it to every downstream component unchanged.
   - C. Silently convert it to a successful action.
   - D. Delete the request.

10. A team optimizes only model quality and ignores latency and cost. What is the
    likely enterprise consequence?
    - A. A technically strong feature may fail its service or budget constraints.
    - B. The model will become deterministic.
    - C. Privacy risk disappears.
    - D. Tests become unnecessary.

## Code reading and debugging

11. Why is this return contract safer than returning the raw provider object?

    ```python
    def call_model(messages: list[dict[str, str]]) -> str:
        response = provider.generate(messages)
        return response.text or ""
    ```

12. A retry wrapper retries every exception three times, including invalid input
    and authentication failure. What is wrong with that policy?

13. A local model and a hosted model produce different output shapes for the same
    task. Where should compatibility logic live?

## Scenario

14. Choose between hosted and local inference for an internal assistant that
    handles sensitive data, has a small pilot load, and needs centralized audit
    logs. State the trade-off and what evidence would change your decision.

## Capstone transfer

15. Specify Chronos’s provider-neutral model boundary, including its inputs,
    normalized output, timeout behavior, and one audit field.
