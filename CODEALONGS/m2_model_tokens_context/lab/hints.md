# Hints

1. Rates are per 1,000 tokens, so divide token counts by 1,000 first.
2. A retained history must never begin with an assistant message; drop that
   first reply if a slice creates one.
3. `instrument` has no model client. Treat `usage` as model output injected
   into your application, so the test is deterministic.

Document one deliberate-forgetting experiment: ask a question whose fact was
removed by trimming, then explain the quality/cost trade-off.
