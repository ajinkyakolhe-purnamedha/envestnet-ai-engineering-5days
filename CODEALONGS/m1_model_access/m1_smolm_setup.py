"""Tiny offline SmolLM helper for M1 snippets."""

import os
from functools import lru_cache
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")

from transformers import pipeline

REPO_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = REPO_ROOT / "OFFLINE-AI-Models" / "smollm2-135m-instruct"


@lru_cache(maxsize=1)
def load_generator():
    return pipeline("text-generation", model=str(MODEL_PATH))


def call_smolm(prompt: str, max_new_tokens: int = 40) -> str:
    result = load_generator()(prompt, max_new_tokens=max_new_tokens, do_sample=False)
    return result[0]["generated_text"]
