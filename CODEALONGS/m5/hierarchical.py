"""Search small. Answer big."""

import numpy as np

from chronos_offline import DATA, embed

text = (DATA / "investment_policy.md").read_text()
parents = ["# " + p.strip()
           for p in text.split("# ") if p.strip()]


# #region parent_child
def split_children(parent: str, size: int = 90):
    """Small units to SEARCH over."""
    words, out, buf = parent.split(), [], []
    for word in words:
        buf.append(word)
        if len(" ".join(buf)) >= size:
            out.append(" ".join(buf))
            buf = []
    return out + ([" ".join(buf)] if buf else [])


children, owner = [], []
for pid, parent in enumerate(parents):
    for child in split_children(parent):
        children.append(child)
        owner.append(pid)              # the link back

index = embed(children)


def retrieve(question: str) -> str:
    """Match on the child. Return the whole parent."""
    best = int(np.argmax(index @ embed([question])[0]))
    return parents[owner[best]]
# #endregion parent_child


print(len(parents), "parents ->", len(children), "children")
print(retrieve("What happens above 35%?").splitlines()[0])

# The unit you SEARCH over and the unit you ANSWER from
# no longer have to be the same size. That is the whole
# idea, and it dissolves the chunk-size argument:
# small children keep the embedding sharp, and the
# parent still arrives with its context intact.
