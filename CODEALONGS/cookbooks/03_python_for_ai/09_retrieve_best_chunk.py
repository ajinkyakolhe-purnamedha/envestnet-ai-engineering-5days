# Retrieve the best chunk
chunks = ["Minimum cash is $2,000.", "Concentration is limited.", "Human confirmation is required."]
scores = [0.9, 0.2, 0.1]
best_chunk = chunks[scores.index(max(scores))]
print(best_chunk)

