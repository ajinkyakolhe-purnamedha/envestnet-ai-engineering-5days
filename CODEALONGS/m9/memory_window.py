"""Memory, made visible: the transcript IS the memory.

Each turn re-sends everything before it, so the prompt grows
every turn — until you window it. Fully offline. Run from
SLIDES-markdown/:
    uv run --project ../CODE-ALONGS python m9/memory_window.py
"""

from chronos_offline import count_tokens

TURNS = [
    ("How is Alice's portfolio doing overall?",
     "Portfolio value is $104,120, up 4.1% overall."),
    ("Which holding is the largest right now?",
     "AAPL is the largest at 52% of total value."),
    ("Is that within our concentration guideline?",
     "No — 52% is above the 35% concentration cap."),
    ("How did it change since last quarter?",
     "The AAPL weight rose from 44% to 52%."),
    ("What about her cash position?",
     "Cash sits at 9%, well inside the 40% cap."),
    ("Why is that a problem for Alice?",
     "One earnings miss now moves half the account."),
]


# #region window
def transcript_tokens(turns: list[str]) -> int:
    return count_tokens(" ".join(turns))


history: list[str] = []
for question, note in TURNS:
    history += [question, note]
    print(f"turn {len(history) // 2}: "
          f"{transcript_tokens(history):>4} tokens")

KEEP = 4  # most recent entries kept verbatim
folded = ("Earlier: "
          + " | ".join(t[:18] for t in history[:-KEEP]))
window = [folded, *history[-KEEP:]]
print(f"windowed: {transcript_tokens(window):>4} tokens")
# #endregion window
