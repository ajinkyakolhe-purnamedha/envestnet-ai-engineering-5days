"""One hosted call to an open-weight model."""

import os

from huggingface_hub import InferenceClient

if token := os.getenv("HF_TOKEN"):
    client = InferenceClient(api_key=token)
    response = client.chat_completion(
        model="Qwen/Qwen3-32B",
        messages=[{"role": "user", "content": "Name one portfolio risk."}],
    )
    print(response.choices[0].message.content)
else:
    print("Set HF_TOKEN in .env to call hosted open-weight inference.")
