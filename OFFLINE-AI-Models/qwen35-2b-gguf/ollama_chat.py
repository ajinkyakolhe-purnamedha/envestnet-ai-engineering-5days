"""One concept: Ollama's Python client talks to the local model server."""

import ollama

response = ollama.chat(
    model="qwen35-2b-chronos",
    messages=[
        {"role": "user", "content": "Name one portfolio risk in one sentence."},
    ],
    think=False,
)

print(response["message"]["content"])
