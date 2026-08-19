"""Search answer-to-answer, not question-to-answer."""

import numpy as np

from chronos_offline import DATA, embed, generate

text = (DATA / "investment_policy.md").read_text()
parts = [p.strip() for p in text.split("# ")
         if "\n" in p.strip()]
titles = [p.split("\n", 1)[0] for p in parts]
bodies = [p.split("\n", 1)[1].strip().replace("\n", " ")
          for p in parts]
index = embed(bodies)

QUESTION = "How much of my money can sit in one stock?"


# #region hyde
def hypothetical(question: str) -> str:
    """Ask for the ANSWER, then search with that instead."""
    return generate(
        [{"role": "user", "content":
          "Write one sentence of formal investment policy "
          f"that would answer: {question}"}],
        max_new_tokens=45,
    )


def search(query_text: str) -> list[tuple[float, str]]:
    scores = index @ embed([query_text])[0]
    order = np.argsort(scores)[::-1][:3]
    return [(scores[i], titles[i]) for i in order]
# #endregion hyde


GOLD = ("No single holding may exceed a fixed percentage of "
        "total portfolio value; positions above that share "
        "are flagged as concentration risk.")

for label, query in [("question", QUESTION),
                     ("HyDE (small)", hypothetical(QUESTION)),
                     ("HyDE (good model)", GOLD)]:
    print(f"\n{label}")
    for score, name in search(query):
        print(f"   {score:.3f}  {name}")

# question            0.722 Cash allocation       <- wrong
#                     0.718 Concentration limit
# HyDE (small)        0.729 Diversification floor  <- no better
#                     0.723 Concentration limit
# HyDE (good model)   0.808 Concentration limit   <- fixed
#                     0.716 Diversification floor
#
# A question and its answer are written in different
# language, so they sit apart in vector space. HyDE
# closes the gap by searching with a fake answer.
#
# But look at row two. Our 135M model wrote generic
# policy-speak with no concentration concept in it, and
# retrieval got no better. HyDE inherits the quality of
# whatever generator you point at it -- so it is the one
# RAG trick you should NOT run on your cheapest model.
