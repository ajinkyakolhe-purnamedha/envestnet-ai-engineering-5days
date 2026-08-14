"""Pattern 3: RAG preview. Retrieve, then answer.

Fully offline. Run:
    uv run --project ../CODE-ALONGS \
        python m3/pattern_rag_preview.py
"""

from chronos_offline import embed, similarity

CHUNKS = [
    "Policy 4.2: no holding may exceed 35% of portfolio value.",
    "Policy 5.1: cash above 40% is flagged for review.",
    "Operations note: market data is point-in-time.",
]


# #region pattern
def retrieve(question: str) -> str:
    q = embed([question])[0]
    vectors = embed(CHUNKS)
    scores = [similarity(q, v) for v in vectors]
    return CHUNKS[scores.index(max(scores))]


def answer(question: str) -> str:
    context = retrieve(question)
    return f"From context: {context}"
# #endregion pattern


if __name__ == "__main__":
    print(answer("What is the single-stock concentration limit?"))

# Pros: current, citable, owned facts. Cons: retrieval
# can miss, distract, or fetch stale chunks. Log the
# chunks first; they are the RAG debugger.
