# M2 advanced answer key

1. A — Fit is not the same as relevance; stale/conflicting context can still degrade quality.
2. A — Input plus reserved output must fit the request budget.
3. A — Durable facts need a separate preservation strategy.
4. A — Tokenizers and special-token handling can differ.
5. A — Joint telemetry supports operational diagnosis and regression.
6. A — Compression must preserve required facts and be checked.
7. A — Similarity is a relevance signal, not truth or authority.
8. A — Better reasoning cannot recover absent or buried evidence reliably.
9. A — Production needs bounded, observable, explicit behavior.
10. A — A budget requires thresholds and actions, not just a number.
11. It ignores input-token cost and returns zero/underestimated total cost when output is small; include both components.
12. Message-role validity depends on the first role and turn boundary, not just list length.
13. Character count does not track tokenizer cost reliably; it can overflow or over-trim. Measure tokens with the target tokenizer/provider estimate and reserve output budget.
14. Trimming is cheap but can lose the constraint; summarization preserves it only if checked; durable state is strongest for a regulated constraint but adds storage/retrieval complexity. Recommend durable typed state plus a test that the constraint appears in every action request.
15. Example fields: request ID, input tokens, output tokens, latency, estimated cost, and overflow/fallback status. Alert at 80% of budget; summarize/trim once, then refuse clearly if still over.
