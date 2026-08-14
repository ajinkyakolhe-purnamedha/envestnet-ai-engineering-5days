"""Fold old turns with the model: summaries are lossy.

The deterministic fold keeps exact words and loses style.
A model summary reads better — check what happens to the
numbers. Fully offline. Run from SLIDES-markdown/:
    uv run --project ../CODE-ALONGS \
        python m9/memory_summarize.py
"""

from chronos_offline import count_tokens, generate

OLD_TURNS = [
    "How is Alice's portfolio doing overall?",
    "Portfolio value is $104,120, up 4.1% overall.",
    "Which holding is the largest right now?",
    "AAPL is 52% of the portfolio, above the 35% cap.",
]

# #region summarize
prompt = ("Summarize this advisor conversation in one "
          "sentence. Keep every number:\n"
          + "\n".join(OLD_TURNS))
summary = generate(prompt, max_new_tokens=48)

print("deterministic fold:")
print("  Earlier: "
      + " | ".join(t[:30] for t in OLD_TURNS))
print("model summary:")
print("  " + summary)
print(f"tokens: {count_tokens(' '.join(OLD_TURNS))} -> "
      f"{count_tokens(summary)}")
# #endregion summarize
