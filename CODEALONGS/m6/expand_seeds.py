"""Turn 300 hand-written seeds into 15,000 rows."""

import random

PROMPT = """Here are 3 advisor notes and the JSON
they map to:

{examples}

Write 5 NEW note/JSON pairs in the same format.
Vary: client names, dates, symbols, sloppy typing,
missing information, notes with no trade at all.
Keep the JSON schema EXACTLY the same."""


# #region expand
def expand(seeds: list[dict], client, rounds: int = 1000):
    rows = []
    for _ in range(rounds):
        shown = random.sample(seeds, 3)
        reply = client.messages.create(
            model="claude-opus-5",
            max_tokens=2048,
            temperature=1.0,     # variety in the INPUT
            messages=[{
                "role": "user",
                "content": PROMPT.format(examples=shown),
            }],
        )
        rows += parse_pairs(reply.content[0].text)
    return rows
# #endregion expand


def parse_pairs(text: str) -> list[dict]:
    ...


# Temperature high for the note, schema rigid for the
# JSON. The rigid half is what you are teaching.
#
# This is the one step in M6 that wants a big model, and
# it is a one-off batch job -- not something on your
# request path. Run it once, keep the output in git.
