"""One concept: meaning search compares embedding vectors, not keywords.

Try:
- Add another policy vector.
- Compare it to the query.
- Explain why similar is not the same as true.
"""

import math


query = [0.90, 0.30]  # "Is this portfolio concentrated?"
concentration_policy = [0.80, 0.35]
cash_policy = [0.20, 0.90]
tax_policy = [0.05, 0.95]
new_policy = [0.70, 0.45]


def cosine(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_length = math.sqrt(sum(a * a for a in left))
    right_length = math.sqrt(sum(b * b for b in right))
    return dot / (left_length * right_length)


scores = {
    "concentration_policy": round(cosine(query, concentration_policy), 3),
    "cash_policy": round(cosine(query, cash_policy), 3),
    "tax_policy": round(cosine(query, tax_policy), 3),
    "new_policy": round(cosine(query, new_policy), 3),
}

for name, score in scores.items():
    print(name, score)
print("\nReal embeddings are high-dimensional learned vectors.")
print("Similarity finds likely context. It does not prove the context is true.")
