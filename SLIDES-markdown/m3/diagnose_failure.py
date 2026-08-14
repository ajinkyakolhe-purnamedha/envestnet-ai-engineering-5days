"""Wrong output -> name the failed dial before changing it.

Fully offline. Run:
    uv run --project ../CODE-ALONGS \
        python m3/diagnose_failure.py
"""


# #region diagnose
def diagnose(observed: str) -> str:
    text = observed.lower()
    if "not in the document" in text:
        return "context"
    if "too long" in text or "wrong format" in text:
        return "instruction"
    if "bad plan" in text or "invalid tool" in text:
        return "model"
    return "inspect trace"
# #endregion diagnose


if __name__ == "__main__":
    for failure in [
        "Invented fee cap; source was not in the document.",
        "Right facts, wrong format: too long.",
        "Bad plan: invalid tool chosen twice.",
    ]:
        print(f"{diagnose(failure):>12}  {failure}")

# A bigger model is the expensive fix. Use it only after
# the cheaper fixes fail. Missing facts usually mean
# context. Wrong shape usually means instruction.
