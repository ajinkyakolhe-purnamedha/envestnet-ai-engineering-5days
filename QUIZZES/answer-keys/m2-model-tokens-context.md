# M2 answer key

1. A — It is the request’s total input budget.
2. A — The application resends the state it wants the model to use.
3. A — Token IDs represent tokenizer pieces numerically.
4. A — The tokenizer and text determine the count.
5. A — All of those request components consume context.
6. A — Each option is an explicit policy with different trade-offs.
7. A — The retained transcript should preserve a valid turn boundary.
8. A — Larger capability often costs more latency and money.
9. A — Instrumentation exposes measurable call behavior.
10. A — Embeddings support semantic comparison, not truth validation.
11. It removes retained assistant messages from the front so the transcript begins with a user turn.
12. System instructions, retained history, and any retrieved or supplied context.
13. It underestimates cost by ignoring input usage; include both input and output token costs.
14. Record the before/after message list, token estimate, retained facts, and resulting quality/cost/latency. Choose a written policy based on the feature’s requirements—for example, summarize durable constraints, trim low-value chatter, retrieve authoritative facts, and reject safely when no valid budget remains.
15. Example: estimate input tokens before the call; if estimated input plus a reserved output budget exceeds the configured limit, summarize or trim low-value history and retry once, otherwise return a clear “conversation too long” message.
