"""Pattern 1: base model call.

Fully offline shape demo. Run:
    uv run --project ../CODE-ALONGS \
        python m3/pattern_base_call.py
"""


def llm(question: str) -> str:
    if "policy" in question.lower():
        return "I think the limit is probably 50%."
    return "Drafted general language."


# #region pattern
def answer(question: str) -> str:
    return llm(question)
# #endregion pattern


if __name__ == "__main__":
    print(answer("Rewrite this client note warmly."))
    print(answer("What is our concentration policy?"))

# Pros: smallest code, fastest path, no retrieval stack.
# Cons: private facts come from memory or invention. Use
# this for language skill, not firm-specific truth.
