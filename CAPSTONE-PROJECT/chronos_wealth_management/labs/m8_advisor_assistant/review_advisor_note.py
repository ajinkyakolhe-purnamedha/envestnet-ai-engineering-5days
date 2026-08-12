"""YOU implement: the quality gate (evaluator pattern, M8.2.5).

The draft is untrusted input until it passes the rules. Deterministic
checks, not model vibes — the cheapest quality gate is an assertion.
"""

MAX_NOTE_WORDS = 80


def review_advisor_note(note: str, verdict: str) -> list[str]:
    """Return the list of problems (empty = the note ships).

    Rules:
    - if the verdict mentions the concentration limit, the note must
      contain "35"
    - if the verdict mentions cash, the note must contain "40"
    - the note stays at or under MAX_NOTE_WORDS words
    """
    raise NotImplementedError("M8 lab step 5: write the evaluator gate")
