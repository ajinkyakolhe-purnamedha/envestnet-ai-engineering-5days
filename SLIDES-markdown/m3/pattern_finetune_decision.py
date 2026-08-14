"""Pattern 4: decide whether fine-tuning is justified.

Fully offline. Run:
    uv run --project ../CODE-ALONGS \
        python m3/pattern_finetune_decision.py
"""


# #region pattern
def choose_customization(problem: str) -> str:
    text = problem.lower()
    if "policy" in text or "latest" in text or "client data" in text:
        return "RAG"
    if "format" in text or "style" in text or "tone" in text:
        return "fine-tune, only if volume justifies labels"
    if "from scratch" in text:
        return "almost never"
    return "prompt first"
# #endregion pattern


if __name__ == "__main__":
    for problem in [
        "Needs latest policy facts.",
        "Must always emit our advisor JSON format.",
        "Train a base model from scratch.",
    ]:
        print(choose_customization(problem), "<-", problem)

# Fine-tuning changes behavior. RAG adds knowledge. If
# the missing thing is a fact, training is usually the
# wrong first move.
