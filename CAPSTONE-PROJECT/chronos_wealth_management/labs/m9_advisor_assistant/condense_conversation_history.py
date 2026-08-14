"""GIVEN: window the conversation history — plumbing, not today's lesson.

The transcript grows every turn and every kept turn is prompt tokens.
This helper keeps the most recent turns verbatim and folds everything
older into one bounded summary line. Deterministic on purpose: replacing
the fold with a SmolLM2-written summary is a lab stretch, not the path.
"""

RECENT_TURNS_TO_KEEP = 4
FOLDED_TURN_PREVIEW_CHARS = 60


def condense_conversation_history(
    history: list[str],
    recent_turns_to_keep: int = RECENT_TURNS_TO_KEEP,
) -> list[str]:
    """Return the history with older turns folded into one line.

    A short history comes back unchanged. A long one becomes
    ``[folded_line, *last_N_turns]`` — bounded, oldest information
    compressed hardest, newest kept word for word.
    """
    if len(history) <= recent_turns_to_keep:
        return list(history)
    older_turns = history[:-recent_turns_to_keep]
    recent_turns = history[-recent_turns_to_keep:]
    folded_line = "Earlier questions: " + " | ".join(
        turn[:FOLDED_TURN_PREVIEW_CHARS] for turn in older_turns
    )
    return [folded_line, *recent_turns]
