"""One question, two places to look."""

import numpy as np

from chronos_offline import DATA, embed

text = (DATA / "investment_policy.md").read_text()
chunks = ["# " + p.strip()
          for p in text.split("# ") if p.strip()]
index = embed(chunks)

QUESTION = ("Is Alice over the concentration limit, and may "
            "her advisor rebalance it for her?")


# #region decompose
def decompose(question: str) -> list[str]:
    """A fast model splits it. Here: the two known asks."""
    return [
        "What is the concentration limit?",
        "May an advisor execute a trade for a client?",
    ]


def search_each(sub_queries: list[str]) -> list[str]:
    """Independent searches, then one merged context."""
    found = []
    for sub in sub_queries:
        best = int(np.argmax(index @ embed([sub])[0]))
        if chunks[best] not in found:
            found.append(chunks[best])
    return found
# #endregion decompose


print("combined question:")
best = int(np.argmax(index @ embed([QUESTION])[0]))
print("   ", chunks[best].splitlines()[0])

print("\ndecomposed:")
subs = decompose(QUESTION)
for sub, hit in zip(subs, search_each(subs)):
    print(f"    {sub}\n      -> {hit.splitlines()[0]}")

# The combined question retrieves ONE chunk, because no
# single passage answers both halves. Whichever half the
# embedding weighted more, the other half is now missing
# from the context -- and the model will happily answer
# anyway, from nothing.
#
# Split first, search independently, merge, then answer.
# In production the splitter is a fast-tier model; the
# hard-coded list above keeps this snippet deterministic.
