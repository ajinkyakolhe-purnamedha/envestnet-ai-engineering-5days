"""A token becomes numbers that mean something.

Run:
    uv run --project ../CODE-ALONGS \
        python m2/embeddings.py
"""

from chronos_offline import embed, similarity

vectors = embed([
    "broad market index fund",       # 0
    "S&P 500 tracker",               # 1
    "leather office chair",          # 2
])

print(vectors.shape)                  # (3, 384)

print(round(similarity(vectors[0], vectors[1]), 3))   # high
print(round(similarity(vectors[0], vectors[2]), 3))   # low

# "index fund" and "S&P 500 tracker" share no words at
# all. Nothing here matched text. It matched MEANING.
#
# 384 numbers per string, and closeness in that space
# is closeness in meaning. That is the entire trick.
#
# Tomorrow you will search over these numbers instead
# of searching over words. That is RAG.
