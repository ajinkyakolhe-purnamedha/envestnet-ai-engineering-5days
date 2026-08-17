"""One concept: compare two small synthetic meaning vectors with cosine similarity."""

from math import sqrt


def cosine(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    denominator = sqrt(sum(a * a for a in left) * sum(b * b for b in right))
    return numerator / denominator


concentration_risk = [0.9, 0.1, 0.0]
large_single_holding = [0.8, 0.2, 0.0]
print(round(cosine(concentration_risk, large_single_holding), 2))
