"""Measure the pipeline in three places, not one."""

import numpy as np

from chronos_offline import DATA, embed, similarity

text = (DATA / "investment_policy.md").read_text()
chunks = ["# " + p.strip()
          for p in text.split("# ") if p.strip()]
index = embed(chunks)

QUESTION = "What is the concentration limit?"
RELEVANT = "Concentration limit"          # the gold label


# #region triad
def context_precision(question: str, k: int = 3) -> float:
    """Of the k chunks we retrieved, how many belong?"""
    order = np.argsort(index @ embed([question])[0])[::-1][:k]
    hits = sum(RELEVANT in chunks[i] for i in order)
    return hits / k


def groundedness(answer: str, context: str) -> float:
    """Best supporting SENTENCE, not the whole chunk.

    Averaging over a chunk buries the one line that
    actually supports the claim. Score per sentence and
    keep the max -- this is what 'faithfulness' means.
    """
    prose = "\n".join(line for line in context.splitlines()
                      if not line.startswith("#"))
    sentences = [s.strip().replace("\n", " ") + "."
                 for s in prose.split(".")
                 if len(s.strip()) > 20]
    a = embed([answer])[0]
    return max(similarity(a, s) for s in embed(sentences))


def answer_relevance(question: str, answer: str) -> float:
    """Does the answer address the question asked?"""
    q, a = embed([question, answer])
    return similarity(q, a)
# #endregion triad


CONTEXT = chunks[0]
for label, answer in [
    ("good", "No holding may exceed 35% of portfolio value."),
    ("hallucinated", "The limit is 60%, set by the SEC."),
    ("evasive", "Concentration is something advisors watch."),
]:
    print(f"{label:>13}  P={context_precision(QUESTION):.2f} "
          f"G={groundedness(answer, CONTEXT):.3f}  "
          f"R={answer_relevance(QUESTION, answer):.3f}")

#          good  P=0.33  G=0.953  R=0.542
#  hallucinated  P=0.33  G=0.635  R=0.622
#       evasive  P=0.33  G=0.790  R=0.634
#
# Read the columns as a diagnosis, not a grade:
#
#   P low          -> retrieval. Re-chunk, hybrid, rerank.
#   P high, G low  -> the model ignored good context.
#                     Fix the prompt, not the retriever.
#   G high, R low  -> it answered a different question.
#
# Now read column R again. It ranks the evasive answer
# ABOVE the correct one. That is not a bug in the code --
# it is the question-to-answer asymmetry from hyde.py,
# showing up in a metric this time instead of a search.
#
# Which is the real lesson of this module: your evaluation
# harness is made of the same fallible parts as your
# pipeline, and it needs its own sanity checks. G is
# trustworthy here because both sides are statements.
# R is not, and shipping it unexamined would have you
# "improving" the system in the wrong direction.
