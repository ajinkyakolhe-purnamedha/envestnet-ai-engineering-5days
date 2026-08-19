"""Where you cut the document decides what you can find."""

from chronos_offline import DATA

text = (DATA / "investment_policy.md").read_text()


# #region strategies
def fixed(text: str, size: int = 200, overlap: int = 40):
    """Blunt, fast, and cuts sentences in half."""
    step = size - overlap
    return [text[i:i + size]
            for i in range(0, len(text), step)]


def structural(text: str):
    """Split on the headings the author already wrote."""
    return [
        "# " + part.strip()
        for part in text.split("# ") if part.strip()
    ]
# #endregion strategies


for name, chunks in [("fixed", fixed(text)),
                     ("structural", structural(text))]:
    sizes = [len(c) for c in chunks]
    print(f"{name:>11}  {len(chunks):>2} chunks  "
          f"min={min(sizes):>3} max={max(sizes):>3}")
    print(f"             first: {chunks[0][:46]!r}")

# Fixed chunks are uniform, which the vector index likes,
# and semantically arbitrary, which retrieval hates: the
# 35% limit can land in one chunk and the word
# "concentration" in the next.
#
# Structural chunks vary in size but never split a rule
# in half. For policy documents, manuals and code, this
# is almost always the right default.
#
# Semantic splitting -- cut where the embedding shifts --
# is the third option. Better boundaries, far slower
# ingestion. Reach for it when structure is absent.
