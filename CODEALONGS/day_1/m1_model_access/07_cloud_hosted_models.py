"""Later: the same models, through your own cloud account.

Nothing here is expected to run in the workshop. It runs once
your organisation gives you a project, an identity and a role.
The call shape is unchanged -- only who holds the key moves.
"""

import os

from dotenv import load_dotenv

load_dotenv(override=True)

PROMPT = "Name one risk in a portfolio with 52% in AAPL."


# #region cloud
def call_vertex(prompt: str) -> str:
    """Gemini through a GCP project and an IAM identity."""
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
    """Open weights that someone else hosts and scales."""
    from huggingface_hub import InferenceClient

    client = InferenceClient(api_key=os.environ["HF_TOKEN"])
    reply = client.chat_completion(
        model="Qwen/Qwen3-32B",
        messages=[{"role": "user", "content": prompt}],
    )
    return reply.choices[0].message.content
# #endregion


CLOUD_PATHS = {
    "GOOGLE_CLOUD_PROJECT": call_vertex,
    "HF_TOKEN": call_hf_inference,
}

for env_name, call_model in CLOUD_PATHS.items():
    if os.getenv(env_name):
        print(f"{env_name}: {call_model(PROMPT)}")
    else:
        print(f"{env_name}: not configured -- expected today")
