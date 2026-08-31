"""One concept: open weights can run from a local folder with no network."""

import os
import warnings
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

from transformers import pipeline
from transformers.utils import logging as transformers_logging

warnings.filterwarnings("ignore", category=FutureWarning)
transformers_logging.set_verbosity_error()

REPO_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = REPO_ROOT / "OFFLINE-AI-Models" / "smollm2-135m-instruct"

print("model folder:", MODEL_PATH)
print("network:", "off")

generate = pipeline("text-generation", model=str(MODEL_PATH))
reply = generate(
    "Name one risk in a portfolio with 52% in AAPL.",
    max_new_tokens=30,
    do_sample=False,
)

print(reply[0]["generated_text"])
