# M2 · Model, tokens, and context — advanced quiz

## Multiple choice

1. A request is below the advertised context limit but still performs poorly
   after several turns. What is the most plausible engineering explanation?
   - A. Embeddings guarantee relevance.
   - B. Stale, conflicting, or distracting history is consuming attention even when it fits.
   - C. The model has no input tokens.
   - D. Context limits apply only to output.

2. Why reserve output budget when estimating whether an input fits?
   - A. It makes the model deterministic.
   - B. Output is generated before input is processed.
   - C. The request must leave room for the intended response as well as input context.
   - D. Output tokens are not charged.

3. Which history strategy best preserves durable account constraints while
   reducing conversational noise?
   - A. Delete the system instruction first.
   - B. Send the complete history forever.
   - C. Keep the last two messages only.
   - D. Summarize or store durable facts separately, then trim low-value turns.

4. Why can token count estimates differ between a local tokenizer and a provider?
   - A. Providers count database rows.
   - B. Local tokenizers count only punctuation.
   - C. They may use different tokenization schemes or special-token rules.
   - D. Token counts depend only on output quality.

5. What is the strongest reason to instrument input tokens, output tokens, latency,
   and cost together?
   - A. It removes the context limit.
   - B. It supports diagnosis of quality/latency/cost trade-offs and regression over time.
   - C. It replaces a test suite.
   - D. It proves the answer is grounded.

6. A summary saves tokens but omits a risk constraint. What does this demonstrate?
   - A. Token counts are irrelevant.
   - B. Retrieval cannot help.
   - C. Summaries always preserve meaning.
   - D. Compression needs a quality/required-fact check, not only a size target.

7. What is the right interpretation of high embedding similarity?
   - A. The text satisfies policy automatically.
   - B. The text should always be returned to the user.
   - C. The text is potentially relevant and should be assessed in context.
   - D. The text is authoritative and true.

8. Why might increasing model size fail to solve a context-grounding problem?
   - A. Larger models never use retrieval.
   - B. Context windows shrink to zero.
   - C. Larger models cannot process tokens.
   - D. The needed fact may be missing, stale, or buried in the supplied context.

9. Which policy best handles repeated context overflow in production?
   - A. Silently discard random messages.
   - B. Increase output length.
   - C. Retry the unchanged request indefinitely.
   - D. Bound the request, apply a documented reduction strategy, observe the result, and fail clearly when necessary.

10. What does a context budget become in a production design?
    - A. A model-training parameter.
    - B. A database index.
    - C. An explicit resource policy with thresholds, actions, and user-visible failure behavior.
    - D. A prompt-writing preference only.

## Code reading and debugging

11. What edge case is missed by this estimator?

    ```python
    def estimate_cost(input_tokens, output_tokens, input_rate, output_rate):
        return output_tokens * output_rate
    ```

12. A history window keeps an even number of messages but sometimes starts with
    an assistant turn. Why is “even number” not enough?

13. A service trims history by character count rather than token count. What
    failure can result, and what should be measured instead?

## Scenario

14. A regulated assistant must retain a client risk constraint for 30 turns,
    but cannot resend all transcript text. Compare trimming, summarization, and
    external durable state, and recommend a design with one verification check.

## Capstone transfer

15. Design Chronos’s context telemetry schema: name four fields, one alert
    threshold, and one action when the threshold is crossed.
