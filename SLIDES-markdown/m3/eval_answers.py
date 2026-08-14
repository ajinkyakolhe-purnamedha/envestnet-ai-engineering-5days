"""'It reads well' is not a metric. These are.

Fully offline. Run:
    uv run --project ../CODE-ALONGS \
        python m3/eval_answers.py
"""

from chronos_offline import embed, similarity

POLICY = "No holding may exceed 35% of portfolio value."


# #region metrics
def groundedness(answer: str, context: str) -> float:
    """Is the answer supported by the context we retrieved?"""
    a, c = embed([answer, context])
    return similarity(a, c)
# #endregion metrics


ANSWERS = {
    "grounded": "Holdings are limited to 35% of the portfolio.",
    "hallucinated": "The limit is 60%, set by the SEC.",
    "off-topic": "Gold has historically hedged inflation.",
}

if __name__ == "__main__":
    for label, answer in ANSWERS.items():
        score = groundedness(answer, POLICY)
        print(f"{label:>13}  grounded={score:.3f}")

#      grounded  grounded=0.825
#  hallucinated  grounded=0.637
#     off-topic  grounded=0.503
#
# Statistical assertions, not exact ones:
#     assert grounded >= 0.70       not  assert x == 42
#
# The honest limit: this metric cannot tell that "60%"
# is false. It only knows the sentence sounds like the
# policy. For facts you can assert, use exact checks.
