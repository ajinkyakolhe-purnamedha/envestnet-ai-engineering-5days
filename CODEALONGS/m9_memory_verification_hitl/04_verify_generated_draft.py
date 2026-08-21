"""One concept: LlamaIndex drafts still need deterministic checks.

Try:
- Remove "35%" from the source facts.
- Lower MAX_WORDS to 15.
- Add a rule requiring the word "AAPL".
"""

from llamaindex_closure_setup import ask_llamaindex, m8_workflow_draft


MAX_WORDS = 35


def review_note(note: str) -> dict[str, object]:
    problems = []
    if len(note.split()) > MAX_WORDS:
        problems.append("too_long")
    if "35%" not in note and "40%" not in note:
        problems.append("missing_threshold")
    return {"passed": not problems, "problems": problems}


m8_output = m8_workflow_draft()
prompt = (
    "Draft a short advisor note from this workflow output. Cite numeric limits.\n"
    f"{m8_output}"
)

generated_draft = ask_llamaindex(prompt, max_tokens=60)
draft = generated_draft if generated_draft and len(generated_draft.split()) <= MAX_WORDS else m8_output["draft"]
review = review_note(draft)

print("generated draft:", generated_draft or "[no new text]")
print("draft:", draft)
print("review:", review)
