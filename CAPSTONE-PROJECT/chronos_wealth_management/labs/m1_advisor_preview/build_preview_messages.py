"""YOU implement: labelled messages for the advisor preview (M1)."""

PREVIEW_INSTRUCTION = (
    "You are Chronos's advisor assistant. Be concise and factual. "
    "Use only the supplied facts."
)


def build_preview_messages(
    context: str,
    question: str,
    previous_questions: list[str],
) -> list[dict[str, str]]:
    """Return system + prior turns + one user message with context and question.

    Hints:
    - system message uses PREVIEW_INSTRUCTION
    - each previous question is its own user turn
    - final user message labels CONTEXT and QUESTION on separate lines
    """
    raise NotImplementedError("M1 lab step 1: build the preview messages")
