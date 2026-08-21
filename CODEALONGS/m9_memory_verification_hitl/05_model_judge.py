"""One concept: a LlamaIndex judge is another model call, so measure it.

Try:
- Change the judge prompt.
- Add a wrong note that still mentions 35%.
- Keep the judge advisory until agreement is measured.
"""

from llamaindex_closure_setup import ask_llamaindex


NOTES = [
    ("AAPL is 52% of portfolio, above the 35% cap.", True),
    ("Cash sits at 48%, above the 40% guideline.", True),
    ("Largest holding exceeds the stated limit.", False),
    ("The portfolio looks fine; no changes needed.", False),
]


def rule_check(note: str) -> bool:
    return "35%" in note or "40%" in note


def model_judge(note: str) -> bool:
    prompt = f'Note: "{note}"\nDoes it cite a threshold percentage? YES or NO.'
    reply = ask_llamaindex(prompt, max_tokens=8)
    return reply.strip().lower().startswith("yes")


judge_results = []
for note, expected in NOTES:
    rule = rule_check(note)
    judge = model_judge(note)
    judge_results.append({"note": note, "expected": expected, "rule": rule, "judge": judge})

agreements = sum(row["rule"] == row["judge"] for row in judge_results)

for row in judge_results:
    print(f"rule={row['rule']!s:5} judge={row['judge']!s:5} {row['note']}")
print(f"agreement with rule: {agreements}/{len(NOTES)}")
