# M2 · Model, tokens, and context — advanced quiz

## Multiple choice

1. A request is below the advertised context limit but still performs poorly
   after several turns. What is the most plausible engineering explanation?
   - A. Stale, conflicting, or distracting history is consuming attention even when it fits.
   - B. The model has no input tokens.
   - C. Context limits apply only to output.
   - D. Embeddings guarantee relevance.

   **Answer: A.** Stale, conflicting, or distracting history can degrade quality even when it fits.
   **Why:** Being under the hard limit does not make context relevant or well prioritized.

2. Why reserve output budget when estimating whether an input fits?
   - A. The request must leave room for the intended response as well as input context.
   - B. Output tokens are not charged.
   - C. Output is generated before input is processed.
   - D. It makes the model deterministic.

   **Answer: A.** The request must leave room for the intended response as well as input context.
   **Why:** Input plus reserved output must fit the request budget.

3. Which history strategy best preserves durable account constraints while
   reducing conversational noise?
   - A. Summarize or store durable facts separately, then trim low-value turns.
   - B. Keep the last two messages only.
   - C. Delete the system instruction first.
   - D. Send the complete history forever.

   **Answer: A.** Preserve durable facts separately, then trim low-value turns.
   **Why:** Important constraints should not depend on lossy recent-history retention.

4. Why can token count estimates differ between a local tokenizer and a provider?
   - A. They may use different tokenization schemes or special-token rules.
   - B. Token counts depend only on output quality.
   - C. Providers count database rows.
   - D. Local tokenizers count only punctuation.

   **Answer: A.** Tokenization schemes and special-token rules can differ.
   **Why:** Token counts are tokenizer-specific measurements.

5. What is the strongest reason to instrument input tokens, output tokens, latency,
   and cost together?
   - A. It supports diagnosis of quality/latency/cost trade-offs and regression over time.
   - B. It proves the answer is grounded.
   - C. It removes the context limit.
   - D. It replaces a test suite.

   **Answer: A.** Joint telemetry supports quality, latency, cost, and regression diagnosis.
   **Why:** The measurements explain which resource or behavior changed.

6. A summary saves tokens but omits a risk constraint. What does this demonstrate?
   - A. Compression needs a quality/required-fact check, not only a size target.
   - B. Summaries always preserve meaning.
   - C. Token counts are irrelevant.
   - D. Retrieval cannot help.

   **Answer: A.** Compression needs a required-fact and quality check, not only a size target.
   **Why:** Saving tokens is unsafe if it removes information required for a decision.

7. What is the right interpretation of high embedding similarity?
   - A. The text is potentially relevant and should be assessed in context.
   - B. The text is authoritative and true.
   - C. The text satisfies policy automatically.
   - D. The text should always be returned to the user.

   **Answer: A.** Similarity indicates potential relevance, not authority or truth.
   **Why:** Retrieved material still needs grounding and policy assessment.

8. Why might increasing model size fail to solve a context-grounding problem?
   - A. The needed fact may be missing, stale, or buried in the supplied context.
   - B. Larger models cannot process tokens.
   - C. Larger models never use retrieval.
   - D. Context windows shrink to zero.

   **Answer: A.** The fact may be absent, stale, or buried in supplied context.
   **Why:** More capability cannot reliably recover missing evidence.

9. Which policy best handles repeated context overflow in production?
   - A. Bound the request, apply a documented reduction strategy, observe the result, and fail clearly when necessary.
   - B. Retry the unchanged request indefinitely.
   - C. Silently discard random messages.
   - D. Increase output length.

   **Answer: A.** Bound the request, reduce context deliberately, observe the result, and fail clearly when necessary.
   **Why:** Production behavior must be predictable under a hard limit.

10. What does a context budget become in a production design?
    - A. An explicit resource policy with thresholds, actions, and user-visible failure behavior.
    - B. A prompt-writing preference only.
    - C. A model-training parameter.
    - D. A database index.

    **Answer: A.** A context budget is an explicit resource policy with thresholds and actions.
    **Why:** A number alone does not define application behavior.

## Code reading and debugging

11. What edge case is missed by this estimator?

    ```python
    def estimate_cost(input_tokens, output_tokens, input_rate, output_rate):
        return output_tokens * output_rate
    ```

    **Answer:** It ignores input-token cost and underestimates total cost.
    **Why:** Input and output may have separate rates and optimization levers.

12. A history window keeps an even number of messages but sometimes starts with
    an assistant turn. Why is “even number” not enough?

    **Answer:** Even length does not guarantee a valid turn boundary.
    **Why:** The retained transcript can still begin with an assistant message and lose the initiating user context.

13. A service trims history by character count rather than token count. What
    failure can result, and what should be measured instead?

    **Answer:** Character count can overflow or over-trim because it does not map reliably to tokens. Measure tokens using the target tokenizer/provider estimate and reserve output budget.
    **Why:** Token usage is the resource actually limited and billed.

## Scenario

14. A regulated assistant must retain a client risk constraint for 30 turns,
    but cannot resend all transcript text. Compare trimming, summarization, and
    external durable state, and recommend a design with one verification check.

    **Expected answer:** Use durable typed state for the risk constraint, then summarize or trim conversational noise. Verify the constraint appears in every action request.
    **Why:** Regulated facts should not depend on lossy transcript compression.

## Capstone transfer

15. Design Chronos’s context telemetry schema: name four fields, one alert
    threshold, and one action when the threshold is crossed.

    **Expected answer:** Fields could include request ID, input/output tokens, latency, estimated cost, and overflow status. Alert at 80%; summarize/trim once and fail clearly if still over.
    **Why:** Telemetry connects resource usage to an operational response.
