"""Rung 2 of the verification ladder: a model as judge.

Six advisor notes — three cite a threshold figure, three
don't. The rule check is exact and free. The model judge is
one more call. Count how often they agree. Fully offline.
Run from SLIDES-markdown/:
    uv run --project ../CODE-ALONGS python m9/llm_judge.py
"""

from chronos_offline import generate

# #region judge
NOTES = [
    ("AAPL is 52% of portfolio, above the 35% cap.", True),
    ("Cash sits at 48%, above the 40% guideline.", True),
    ("Largest holding 52% exceeds the 35% limit.", True),
    ("The portfolio looks fine; no changes needed.", False),
    ("Alice should feel good about her positions.", False),
    ("Holdings are broadly balanced at this time.", False),
]


def rule_check(note: str) -> bool:  # rung 1: exact, free
    return "35%" in note or "40%" in note


def model_judge(note: str) -> bool:  # rung 2: +1 call
    reply = generate(
        f'Note: "{note}"\nDoes the note cite a specific '
        "threshold percentage? Answer YES or NO.",
        max_new_tokens=8)
    return reply.strip().lower().startswith("yes")


agreements = 0
for note, cites in NOTES:
    rule, judge = rule_check(note), model_judge(note)
    agreements += rule == judge
    print(f"rule={rule!s:5} judge={judge!s:5} {note[:40]}")
print(f"agreement with the rule: {agreements}/6")
# #endregion judge
