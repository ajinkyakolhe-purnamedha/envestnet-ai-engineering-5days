"""An open-weight model that runs here. No network at all."""

import os
from pathlib import Path

from transformers import pipeline

# Fail loudly instead of silently downloading at the venue.
os.environ.setdefault("HF_HUB_OFFLINE", "1")

REPO_ROOT = Path(__file__).resolve().parents[3]
MODELS = REPO_ROOT / "OFFLINE-AI-Models"

# How these weights got here, once, on a networked machine:
#
#   from huggingface_hub import snapshot_download
#
#   snapshot_download(
#       "HuggingFaceTB/SmolLM2-135M-Instruct",
#       local_dir=MODELS / "smollm2-135m-instruct",
#   )
#
# Any Hub model id works the same way. This repo ships one
# already, so nothing downloads while thirty people run it.

# #region run
MODEL_PATH = MODELS / "smollm2-135m-instruct"

generate = pipeline(
    "text-generation",
    model=str(MODEL_PATH),
)

reply = generate(
    "Name one risk in a portfolio with 52% in AAPL.",
    max_new_tokens=30,
)
print(reply[0]["generated_text"])
# #endregion
