# M2 answer key

1. A — The context window limits all request context.
2. A — The application resends state for a stateless call.
3. A — Tokenization depends on vocabulary and tokenizer rules.
4. A — All listed request components consume context.
5. A — Unbounded history creates limit, cost, latency, and distraction risks.
6. A — The application must choose and document a policy.
7. A — A coherent turn boundary preserves meaning and protocol validity.
8. A — Input and output have different economics and optimization levers.
9. A — Embeddings support similarity search, not truth or policy.
10. A — Larger models commonly use more compute and cost more.
11. It retains the most recent `keep_turns * 2` messages; it does not ensure the slice begins with a user message or fit the model’s token budget.
12. Input-token usage is missing, so the estimate understates total cost and may hide the largest optimization opportunity.
13. The conversation may have an invalid or confusing boundary. Remove leading assistant messages or retain a complete recent turn, then test the resulting transcript.
14. Measure input/output tokens, latency, cost, truncation/fallback rate, and whether required facts remain. Start with a bounded recent-turn policy plus a summary or durable-fact path for information that must survive.
15. Example: estimate request tokens plus a reserved output budget; when a threshold is crossed, summarize/trim low-value history and retry once; if still over budget, return a clear “conversation too long” message without calling the model.
