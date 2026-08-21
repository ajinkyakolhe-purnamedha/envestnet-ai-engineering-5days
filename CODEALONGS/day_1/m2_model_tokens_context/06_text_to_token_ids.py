"""One concept: model text becomes token IDs before the model can use it.

Try:
- Encode a ticker.
- Encode a sentence.
- Compare token count with character count.
"""

import tiktoken


model = "gpt-4o-mini"
text = "AAPL concentration risk"

encoder = tiktoken.encoding_for_model(model)
token_ids = encoder.encode(text)
tokens = [encoder.decode([token_id]) for token_id in token_ids]
comparison_texts = ["AAPL", "portfolio concentration", "sell 40 shares"]
comparisons = [(item, len(item), len(encoder.encode(item)), encoder.encode(item)) for item in comparison_texts]

print("text     ", text)
print("token ids", token_ids)
print("tokens   ", tokens)
for item, characters, token_count, ids in comparisons:
    print(item, "characters", characters, "tokens", token_count, ids)
