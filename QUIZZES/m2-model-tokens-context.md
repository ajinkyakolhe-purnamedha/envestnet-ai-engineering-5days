# M2 · Model, tokens, and context quiz

## Multiple choice

1. What is the context window?
   - A. The total limit on the instructions, history, and other input the model can process for a request.
   - B. The model’s training-data size.
   - C. The network timeout.
   - D. The number of users in a database.

2. Why does a stateless model call resend history?
   - A. The application owns the conversation state and must include relevant history in each request.
   - B. The server remembers every user forever.
   - C. Tokens are stored in SQLite automatically.
   - D. The model can only read one word.

3. What is a token ID?
   - A. A numeric representation used by a tokenizer for a piece of text
   - B. An API credential
   - C. A database primary key for a portfolio
   - D. A latency measurement

4. Why are token counts evidence rather than exact universal truths?
   - A. Tokenization depends on the tokenizer and the text.
   - B. Every language uses the same token IDs.
   - C. Counts are unrelated to input.
   - D. Tokens only exist during training.

5. What contributes to the context consumed by a request?
   - A. System instructions, retained history, current input, and any included context
   - B. Only the user’s final question
   - C. Only the output tokens
   - D. The Python interpreter version

6. When history grows too large, which is an explicit engineering choice?
   - A. Trim old turns, summarize them, retrieve relevant facts, or reject the request with a clear policy.
   - B. Pretend the context limit does not exist.
   - C. Delete the system instruction first without review.
   - D. Increase the model’s parameter count at runtime.

7. Why must trimmed chat history begin with a valid user message?
   - A. An assistant-leading transcript can violate the expected turn structure.
   - B. User messages are always shorter.
   - C. It reduces the model’s parameter count.
   - D. It makes embeddings exact.

8. What does a larger model generally trade for higher capability?
   - A. More latency and cost, subject to the specific model and workload
   - B. Fewer parameters and no quality change
   - C. Guaranteed factuality
   - D. Zero context usage

9. What does instrumentation make visible?
   - A. Input/output usage, duration, and estimated cost for a call
   - B. The model’s private training examples
   - C. A guarantee that the answer is true
   - D. The user’s password

10. What are embeddings primarily useful for?
   - A. Comparing semantic similarity between pieces of text
   - B. Replacing all validation rules
   - C. Counting HTTP retries
   - D. Selecting a Python interpreter

## Code reading and debugging

11. Given `trim_history(history, keep_turns=1)` and a history ending with a
    user message, what does the function’s `while` loop protect against?

12. A developer counts only the latest question and concludes that the request
    is below the context limit. Which input parts did they omit?

13. A cost report uses only `output_tokens * output_rate`. What accounting bug
    does this create, and what should the estimate include?

## Scenario

14. In the M2 lab, a Chronos transcript has become too long and the assistant
    loses the first portfolio constraint after trimming. What evidence should
    the learner record, and what policy should they choose between trimming,
    summarizing, retrieval, or rejection?

## Capstone transfer

15. Design one context-budget guard for a Chronos portfolio assistant. State the
    measurement, threshold decision, and user-visible behavior when the budget
    is exceeded.
