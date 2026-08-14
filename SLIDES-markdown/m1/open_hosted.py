"""Way 4: open model, someone else's GPU.

Run:
    uv run --project ../CODE-ALONGS \
        python m1/open_hosted.py
"""

import os


# #region call
def call_hosted_open_model(prompt: str) -> str:
    from huggingface_hub import InferenceClient

    client = InferenceClient(api_key=os.environ["HF_TOKEN"])

    out = client.chat_completion(
        model="Qwen/Qwen3-235B-A22B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
    )
    return out.choices[0].message.content
# #endregion call


if __name__ == "__main__":
    if os.getenv("HF_TOKEN"):
        print(call_hosted_open_model("Name one risk."))
    else:
        print("No HF_TOKEN set -- not calling out.")

# Same weights you could run yourself -- rented compute.
# Move to your own GPUs later and this code does not
# change. You need a key here, but not permission:
# nobody can revoke your right to these weights.
