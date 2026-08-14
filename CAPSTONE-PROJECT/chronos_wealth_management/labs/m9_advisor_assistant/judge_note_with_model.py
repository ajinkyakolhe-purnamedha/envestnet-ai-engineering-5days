"""STRETCH — implement if time allows: the model judge (M9.3.3, rung 2).

A second opinion bought with one more model call: ask the model whether
the drafted note is consistent with the already-decided verdict. It is
ADVISORY ONLY — the approval queue displays it next to the rule check
and the human decides. You measured this morning how far a 135M judge
can be trusted; that measurement is why it never blocks.

Until implemented, the queue's judge column simply shows nothing and
two lab tests stay skipped.
"""

from labs.m9_advisor_assistant.model_loading import (
    load_offline_language_model,
)

JUDGE_YES = "YES"
JUDGE_NO = "NO"


def judge_note_with_model(note: str, verdict: str | None) -> str | None:
    """Return JUDGE_YES / JUDGE_NO, or None when no model is installed.

    Hints:
    - generator = load_offline_language_model(); None -> return None
      (the rung is skipped, never faked)
    - prompt with the note and the verdict marked as already decided,
      and ask ONE yes/no question: does the note state this verdict
      and its threshold figure? End with "Answer YES or NO."
    - call shape, same as the M8 draft step:
        out = generator([{"role": "user", "content": prompt}],
                        max_new_tokens=10)
        reply = out[0]["generated_text"][-1]["content"]
    - parse defensively: small models ramble. Look for "yes" in the
      first few words of the lowercased reply; anything else — hedges,
      apologies, essays — counts as JUDGE_NO
    """
    raise NotImplementedError("M9 lab stretch: ask the model to judge")
