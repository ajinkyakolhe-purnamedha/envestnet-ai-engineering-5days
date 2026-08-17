# M2 · Model, tokens, and context quiz

## Multiple choice

1. What is a context window?
   - A. The maximum request context a model can process, including instructions, history, and supplied material.
   - B. The amount of training data a model has seen.
   - C. The number of users an application supports.
   - D. The network timeout for an API call.

2. Why does a stateless model call usually need conversation history from the
   application?
   - A. The application owns the state and must resend the relevant context.
   - B. The model permanently remembers every conversation.
   - C. History is stored automatically in the tokenizer.
   - D. The provider stores business rules for the application.

3. Why can two tokenizers produce different token counts for the same text?
   - A. Token boundaries depend on the tokenizer and its vocabulary.
   - B. Token counts are random at runtime.
   - C. Output length changes the input text.
   - D. Tokens are database rows.

4. Which parts should be included when estimating request context?
   - A. System instructions, retained history, current input, and any retrieved or supplied context.
   - B. Only the final user question.
   - C. Only output tokens.
   - D. Only the model name.

5. What is the main risk of allowing conversation history to grow without a
   policy?
   - A. Requests can exceed limits, become slower/costlier, or distract the model with stale information.
   - B. The model gains permanent memory.
   - C. The application stops needing validation.
   - D. The database schema changes automatically.

6. Which policy is most appropriate when history no longer fits the budget?
   - A. Select deliberately among trimming, summarization, retrieval, or a clear refusal.
   - B. Delete the system instruction silently.
   - C. Retry indefinitely with the same request.
   - D. Assume the provider will truncate the right information.

7. Why should a trimmed chat transcript preserve valid turn order?
   - A. The model and application need a coherent conversation boundary to interpret the messages.
   - B. Assistant messages cannot contain text.
   - C. User messages always cost less.
   - D. Turn order changes the model’s weights.

8. Why should input and output usage be measured separately?
   - A. They can have different cost, latency, and optimization strategies.
   - B. Only output contributes to cost.
   - C. Input tokens are never processed.
   - D. Separate measurements make answers deterministic.

9. What can embeddings help an application do?
   - A. Compare semantic similarity and find potentially relevant text.
   - B. Prove that a statement is true.
   - C. Enforce every business policy.
   - D. Replace the application database.

10. Why might a larger model increase operational cost even when the prompt is
    unchanged?
    - A. Larger models often require more compute and may be slower or priced higher.
    - B. Larger models use no context.
    - C. Larger models remove all retries.
    - D. Parameter size affects only the user interface.

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
