# M2 · Model, tokens, and context quiz

## Multiple choice

1. What is a context window?
   - A. The maximum request context a model can process, including instructions, history, and supplied material.
   - B. The amount of training data a model has seen.
   - C. The number of users an application supports.
   - D. The network timeout for an API call.

   **Answer: A.** It is the maximum request context a model can process.
   **Why:** Instructions, history, current input, and supplied material all consume the request budget.

2. Why does a stateless model call usually need conversation history from the
   application?
   - A. The application owns the state and must resend the relevant context.
   - B. The model permanently remembers every conversation.
   - C. History is stored automatically in the tokenizer.
   - D. The provider stores business rules for the application.

   **Answer: A.** The application owns the state and must resend relevant context.
   **Why:** A stateless call does not automatically remember earlier turns.

3. Why can two tokenizers produce different token counts for the same text?
   - A. Token boundaries depend on the tokenizer and its vocabulary.
   - B. Token counts are random at runtime.
   - C. Output length changes the input text.
   - D. Tokens are database rows.

   **Answer: A.** Token boundaries depend on the tokenizer and its vocabulary.
   **Why:** Different tokenizers can split the same text differently.

4. Which parts should be included when estimating request context?
   - A. System instructions, retained history, current input, and any retrieved or supplied context.
   - B. Only the final user question.
   - C. Only output tokens.
   - D. Only the model name.

   **Answer: A.** Include system instructions, retained history, current input, and supplied context.
   **Why:** All of those parts contribute to the request context.

5. What is the main risk of allowing conversation history to grow without a
   policy?
   - A. Requests can exceed limits, become slower/costlier, or distract the model with stale information.
   - B. The model gains permanent memory.
   - C. The application stops needing validation.
   - D. The database schema changes automatically.

   **Answer: A.** Unbounded history can exceed limits, increase cost/latency, and distract the model.
   **Why:** History needs an explicit retention policy.

6. Which policy is most appropriate when history no longer fits the budget?
   - A. Select deliberately among trimming, summarization, retrieval, or a clear refusal.
   - B. Delete the system instruction silently.
   - C. Retry indefinitely with the same request.
   - D. Assume the provider will truncate the right information.

   **Answer: A.** Choose deliberately among trimming, summarization, retrieval, or clear refusal.
   **Why:** The application must control which information is preserved or discarded.

7. Why should a trimmed chat transcript preserve valid turn order?
   - A. The model and application need a coherent conversation boundary to interpret the messages.
   - B. Assistant messages cannot contain text.
   - C. User messages always cost less.
   - D. Turn order changes the model’s weights.

   **Answer: A.** The model and application need a coherent conversation boundary.
   **Why:** A valid turn structure helps the model interpret retained history.

8. Why should input and output usage be measured separately?
   - A. They can have different cost, latency, and optimization strategies.
   - B. Only output contributes to cost.
   - C. Input tokens are never processed.
   - D. Separate measurements make answers deterministic.

   **Answer: A.** Input and output can have different cost, latency, and optimization strategies.
   **Why:** Separate measurements show where resource use is coming from.

9. What can embeddings help an application do?
   - A. Compare semantic similarity and find potentially relevant text.
   - B. Prove that a statement is true.
   - C. Enforce every business policy.
   - D. Replace the application database.

   **Answer: A.** Embeddings help compare semantic similarity and find potentially relevant text.
   **Why:** Similarity is a retrieval signal, not proof of truth or policy compliance.

10. Why might a larger model increase operational cost even when the prompt is
    unchanged?
    - A. Larger models often require more compute and may be slower or priced higher.
    - B. Larger models use no context.
    - C. Larger models remove all retries.
   - D. Parameter size affects only the user interface.

   **Answer: A.** Larger models often require more compute and may be slower or costlier.
   **Why:** Model capability choices have operational consequences.

## Code reading and debugging

11. What does this expression retain, and what important question does it not
    answer?

    ```python
    retained = messages[-(keep_turns * 2):]
    ```

    **Answer:** It retains the most recent `keep_turns * 2` messages, but does not prove that the slice begins with a user turn or fits the token budget.
    **Why:** Message count and token/context validity are separate concerns.

12. A cost estimate uses only `output_tokens * output_rate`. What is missing,
    and why does it matter?

    **Answer:** Input-token usage and its rate are missing.
    **Why:** Ignoring input usage understates total cost and hides an optimization opportunity.

13. A trimming function returns a list whose first message has role `assistant`.
    What could go wrong, and what is one corrective step?

    **Answer:** The transcript may have an invalid or confusing boundary. Remove leading assistant messages or retain a complete recent turn.
    **Why:** A coherent turn structure is part of a valid conversation request.

## Scenario

14. A production assistant becomes slower and more expensive as users continue
    chatting. What measurements would you collect, and how would you choose an
    initial history policy without losing important facts?

    **Expected answer:** Measure input/output tokens, latency, cost, fallback rate, and whether required facts remain. Start with bounded recent history plus summarization or durable-fact storage.
    **Why:** The policy must reduce resource use while preserving information the feature requires.

## Capstone transfer

15. Define a context-budget guard for Chronos: what will be measured, when will
    it act, and what will the user see if the budget cannot be met?

    **Expected answer:** Estimate request tokens plus reserved output; trim/summarize when a threshold is crossed, retry once, and show a clear “conversation too long” message if still over.
    **Why:** A guard turns a hard model limit into predictable application behavior.
