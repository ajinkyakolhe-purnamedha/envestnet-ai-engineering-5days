"""One concept: LiteLLM routes the same completion() call to Ollama."""

from litellm import completion

response = completion(
    model="ollama/qwen35-2b-chronos",
    api_base="http://localhost:11434",
    messages=[
        {"role": "user", "content": "Name one portfolio risk in one sentence."},
    ],
    max_tokens=80,
    temperature=0.2,
    think=False,
)

print(response.choices[0].message.content)
