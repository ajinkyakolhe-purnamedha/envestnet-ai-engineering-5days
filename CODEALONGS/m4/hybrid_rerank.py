"""Dense finds meaning. Sparse finds exact strings."""

import math
from collections import Counter

import numpy as np

from chronos_offline import DATA, embed

text = (DATA / "investment_policy.md").read_text()
chunks = ["# " + p.strip()
          for p in text.split("# ") if p.strip()]
index = embed(chunks)


# #region hybrid
def bm25(query: str, docs: list[str]) -> np.ndarray:
    """Sparse keyword scoring. Exact terms, no semantics."""
    tokens = [d.lower().split() for d in docs]
    avg = sum(len(t) for t in tokens) / len(tokens)
    scores = np.zeros(len(docs))

    for term in query.lower().split():
        n = sum(term in t for t in tokens)
        if not n:
            continue
        idf = math.log(1 + (len(docs) - n + 0.5) / (n + 0.5))
        for i, doc in enumerate(tokens):
            tf = Counter(doc)[term]
            norm = 1 - 0.75 + 0.75 * len(doc) / avg
            scores[i] += idf * tf * 2.5 / (tf + 1.5 * norm)
    return scores


def fuse(dense: np.ndarray, sparse: np.ndarray, k: int = 60):
    """Reciprocal rank fusion -- ranks, not raw scores."""
    out = np.zeros(len(dense))
    for s in (dense, sparse):
        for rank, i in enumerate(np.argsort(s)[::-1]):
            out[i] += 1 / (k + rank)
    return out
# #endregion hybrid


def title(scores) -> str:
    return chunks[int(np.argmax(scores))].splitlines()[0][2:]


for question in ["35%", "Who signs off before anything?"]:
    dense = index @ embed([question])[0]
    sparse = bm25(question, chunks)
    print(f"\n{question}")
    print(f"   dense   {title(dense)}")
    print(f"   sparse  {title(sparse)}")
    print(f"   hybrid  {title(fuse(dense, sparse))}")

# 35%
#    dense   Cash allocation          <- wrong. 40% is also
#    sparse  Concentration limit         a percentage.
#    hybrid  Concentration limit
#
# Who signs off before anything happens?
#    dense   Human confirmation
#    sparse  Concentration limit      <- wrong. The chunk
#    hybrid  Human confirmation          shares no words.
#
# Each method fails alone, in opposite directions, and
# fusion survives both. That is the whole argument for
# hybrid search -- not that it is cleverer, but that its
# two halves fail on different queries.
#
# Production adds a third stage: over-fetch 20 candidates
# here, then a CROSS-ENCODER re-scores each (query, chunk)
# pair jointly and keeps 3. Slower per pair, far more
# accurate -- and it needs a second model we do not ship
# offline, so this is where the demo stops.
