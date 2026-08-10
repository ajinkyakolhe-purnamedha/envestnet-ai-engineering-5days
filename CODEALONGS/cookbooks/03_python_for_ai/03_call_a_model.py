# Call an OpenAI-compatible model
import os
from openai import OpenAI

endpoint = os.getenv("MODEL_ENDPOINT")
key = os.getenv("MODEL_API_KEY")
model = os.getenv("MODEL_NAME")
if endpoint and key and model:
    client = OpenAI(base_url=endpoint, api_key=key)
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": "Say hello."}]
    )
    print(response.choices[0].message.content)
else:
    print("Set MODEL_ENDPOINT, MODEL_API_KEY and MODEL_NAME to call a model.")

