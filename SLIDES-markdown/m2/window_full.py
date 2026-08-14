"""The window is finite. Decide what falls out.

Run:
    uv run --project ../CODE-ALONGS \
        python m2/window_full.py
"""

# #region trim
KEEP_TURNS = 20


def trim(messages: list[dict]) -> list[dict]:
    """Drop the oldest turns, keep the transcript valid."""
    keep = messages[-KEEP_TURNS:]

    # A transcript must start on a user turn, and a tool
    # result must never be orphaned from its tool call.
    while keep and keep[0]["role"] != "user":
        keep.pop(0)
    return keep
# #endregion trim


history = [
    {"role": "user" if i % 2 == 0 else "assistant",
     "content": f"turn {i}"}
    for i in range(30)
]
print(len(history), "->", len(trim(history)))

# How you find out you overflowed -- check stop_reason:
#
#   "max_tokens"
#       The REPLY was cut off mid-sentence.
#       Fix: raise max_tokens, or stream.
#
#   "model_context_window_exceeded"
#       The INPUT no longer fits.
#       Fix: trim old turns, or summarise them.
#
# Trimming forgets. Summarising remembers, but costs a
# call -- and the summary is itself a lossy compression
# you will one day have to debug.
