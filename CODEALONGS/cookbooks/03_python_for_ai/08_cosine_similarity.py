# Cosine similarity
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

query = np.array([[1.0, 0.0]])
documents = np.array([[0.8, 0.2], [0.0, 1.0]])
scores = cosine_similarity(query, documents)
print(scores)

