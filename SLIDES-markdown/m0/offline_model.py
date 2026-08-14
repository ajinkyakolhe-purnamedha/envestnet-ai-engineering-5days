"""Pull a $200M artifact onto your laptop. For free.

Run:
    uv run --project ../CODE-ALONGS \
        python m0/offline_model.py
"""

# Run ONCE, on a machine with network. The weights then
# live in a folder you own:
#
#   from huggingface_hub import snapshot_download
#   snapshot_download(
#       repo_id="HuggingFaceTB/SmolLM2-135M-Instruct",
#       local_dir="OFFLINE-AI-Models/smollm2-135m-instruct",
#       ignore_patterns=["*.msgpack", "*.h5", "onnx/*"],
#   )
#
# For this workshop that already happened -- the weights
# are committed to the repo. Nothing below touches the
# network.

from chronos_offline import generate

reply = generate(
    "In one sentence: what is a concentrated portfolio?",
    max_new_tokens=40,
)
print(reply)

# 260 MB of numbers, sitting in your repo. No API key.
# No per-token bill. No data leaving the box.
#
# It is small enough to be wrong, and yours enough to
# fine-tune. Both of those matter later.
