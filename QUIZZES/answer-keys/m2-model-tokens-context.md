# M2 answer key

1. A — A token is a piece of text used by the model.
2. A — The context window is the request-processing limit.
3. A — Those are the main request components.
4. A — The application resends the state needed for a stateless call.
5. A — Counts help estimate limits and operating cost.
6. A — Size needs an explicit handling policy.
7. A — Trimming can remove important facts or break turn order.
8. A — Input usage measures processed request text.
9. A — Production quality includes operational constraints.
10. A — Embeddings support semantic comparison.
11. The last four messages.
12. It ignores input-token cost; a complete estimate includes input and output usage.
13. The transcript may have an invalid turn boundary. Remove leading assistant messages or retain a complete user/assistant turn.
14. Collect token/input size and latency/cost measurements; try a recent-history limit or summarization policy.
15. Example: estimate input tokens before each call and trim or summarize low-value history when a threshold is reached.
