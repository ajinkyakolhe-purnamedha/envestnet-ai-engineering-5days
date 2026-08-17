# M2 · Model, tokens, and context quiz

## Multiple choice

1. What is a context window?
   - A. The network timeout for an API call.
   - B. The maximum request context a model can process, including instructions, history, and supplied material.
   - C. The amount of training data a model has seen.
   - D. The number of users an application supports.

2. Why does a stateless model call usually need conversation history from the
   application?
   - A. The provider stores business rules for the application.
   - B. The model permanently remembers every conversation.
   - C. The application owns the state and must resend the relevant context.
   - D. History is stored automatically in the tokenizer.

3. Why can two tokenizers produce different token counts for the same text?
   - A. Tokens are database rows.
   - B. Output length changes the input text.
   - C. Token boundaries depend on the tokenizer and its vocabulary.
   - D. Token counts are random at runtime.

4. Which parts should be included when estimating request context?
   - A. Only output tokens.
   - B. Only the model name.
   - C. Only the final user question.
   - D. System instructions, retained history, current input, and any retrieved or supplied context.

5. What is the main risk of allowing conversation history to grow without a
   policy?
   - A. The database schema changes automatically.
   - B. Requests can exceed limits, become slower/costlier, or distract the model with stale information.
   - C. The model gains permanent memory.
   - D. The application stops needing validation.

6. Which policy is most appropriate when history no longer fits the budget?
   - A. Retry indefinitely with the same request.
   - B. Assume the provider will truncate the right information.
   - C. Select deliberately among trimming, summarization, retrieval, or a clear refusal.
   - D. Delete the system instruction silently.

7. Why should a trimmed chat transcript preserve valid turn order?
   - A. User messages always cost less.
   - B. Turn order changes the model’s weights.
   - C. Assistant messages cannot contain text.
   - D. The model and application need a coherent conversation boundary to interpret the messages.

8. Why should input and output usage be measured separately?
   - A. Input tokens are never processed.
   - B. They can have different cost, latency, and optimization strategies.
   - C. Separate measurements make answers deterministic.
   - D. Only output contributes to cost.

9. What can embeddings help an application do?
   - A. Enforce every business policy.
   - B. Replace the application database.
   - C. Compare semantic similarity and find potentially relevant text.
   - D. Prove that a statement is true.

10. Why might a larger model increase operational cost even when the prompt is
    unchanged?
    - A. Parameter size affects only the user interface.
    - B. Larger models use no context.
    - C. Larger models often require more compute and may be slower or priced higher.
    - D. Larger models remove all retries.

## Code reading and debugging

11. What does this expression retain, and what important question does it not
    answer?

    ```python
    retained = messages[-(keep_turns * 2):]
    ```

12. A cost estimate uses only `output_tokens * output_rate`. What is missing,
    and why does it matter?

13. A trimming function returns a list whose first message has role `assistant`.
    What could go wrong, and what is one corrective step?

## Scenario

14. A production assistant becomes slower and more expensive as users continue
    chatting. What measurements would you collect, and how would you choose an
    initial history policy without losing important facts?

## Capstone transfer

15. Define a context-budget guard for Chronos: what will be measured, when will
    it act, and what will the user see if the budget cannot be met?
