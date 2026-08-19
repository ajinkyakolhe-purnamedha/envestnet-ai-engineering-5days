"""RAG in five steps, none of them hidden."""

import numpy as np

from chronos_offline import DATA, embed, generate

QUESTION = "How much of the portfolio can one holding be?"


# #region pipeline
# 1. Load
text = (DATA / "investment_policy.md").read_text()

# 2. Chunk -- on headings, so no rule is cut in half
chunks = ["# " + p.strip()
          for p in text.split("# ") if p.strip()]

# 3. Embed once, at ingestion time
index = embed(chunks)

# 4. Retrieve -- cosine against every chunk
scores = index @ embed([QUESTION])[0]
top = np.argsort(scores)[::-1][:2]
context = "\n\n".join(chunks[i] for i in top)

# 5. Generate, grounded in what we retrieved
answer = generate(
    [{"role": "user", "content":
      f"Use only this policy:\n{context}\n\nQ: {QUESTION}"}],
    max_new_tokens=60,
)
# #endregion pipeline

for i in top:
    print(f"  {scores[i]:.3f}  {chunks[i].splitlines()[0]}")
print("\n", answer)

#   0.808  # Concentration limit      <- correct chunk
#   0.767  # Diversification floor
#
#   "To determine how much of the portfolio can one
#    holding be, we need to calculate the total portfolio
#    value. Total portfolio value = Total portfolio
#    assets + Total portfolio assets - ..."
#
# Read those two halves separately, because they fail
# separately. RETRIEVAL WORKED: the right rule came back
# top, at 0.808. GENERATION FAILED: a 135M model was
# handed the answer and still produced arithmetic soup.
#
# Almost every team seeing this output says "the
# retrieval is broken" and starts re-chunking. Here that
# would be a week spent fixing the half that worked.
# Telling those two apart is a measurement problem, and
# it is exactly what M5 is about.
#
# A vector database replaces steps 3 and 4 when `index`
# stops fitting in RAM -- it does not add a concept you
# have not just seen. LlamaIndex writes all five as:
#   index = VectorStoreIndex.from_documents(docs)
#   index.as_query_engine().query(QUESTION)
# Convenient, and worth having built once by hand first.
