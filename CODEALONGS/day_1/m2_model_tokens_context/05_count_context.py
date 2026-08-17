"""One concept: count the words in one assembled request as a simple estimate."""

prompt = "You are concise. AAPL is 52% of the portfolio. What is the risk?"
estimated_tokens = len(prompt.split())

print(f"Estimated input tokens: {estimated_tokens}")
