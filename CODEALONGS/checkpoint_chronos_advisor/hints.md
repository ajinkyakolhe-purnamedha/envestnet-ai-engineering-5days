# Hints

1. For bounded history, the newest four messages are `history[-4:]`.
2. For evidence, return `None` if the best policy passage has zero meaningful
   words in common with the question.
3. For the agent, use `json.loads` before dispatching. Treat a JSON parse
   error or an unlisted tool as a controlled refusal.
