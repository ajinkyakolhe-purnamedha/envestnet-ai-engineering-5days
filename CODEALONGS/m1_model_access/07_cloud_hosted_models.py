"""One concept: governed cloud access changes who vouches for the caller."""

import os

from dotenv import load_dotenv

load_dotenv(override=True)

PROMPT = "Name one risk in a portfolio with 52% in AAPL."


def call_vertex(prompt: str) -> str:
    from google import genai

    client = genai.Client(
        vertexai=True,
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location="global",
    )
    reply = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )
    return reply.text


def call_hf_inference(prompt: str) -> str:
    from huggingface_hub import InferenceClient

    client = InferenceClient(api_key=os.environ["HF_TOKEN"])
    reply = client.chat_completion(
        model="Qwen/Qwen3-32B",
        messages=[{"role": "user", "content": prompt}],
    )
    return reply.choices[0].message.content


print("Direct provider key -> individual application secret")
print("Cloud model platform -> project, identity, role, audit")
print("GOOGLE_CLOUD_PROJECT:", os.getenv("GOOGLE_CLOUD_PROJECT") or "not configured")
print("HF_TOKEN:", "configured" if os.getenv("HF_TOKEN") else "not configured")
