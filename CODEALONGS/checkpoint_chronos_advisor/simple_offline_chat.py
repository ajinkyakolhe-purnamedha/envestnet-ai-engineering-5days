"""The smallest useful Chronos call to the local offline model."""

from offline_model import generate

messages = [
    {"role": "system", "content": "You are a concise educational investor assistant."},
    {"role": "user", "content": "Explain diversification in one sentence."},
]

print(generate(messages, max_new_tokens=60))
