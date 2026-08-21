"""Tiny offline SmolLM helper for M2 snippets."""

import os
from functools import lru_cache
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")

from transformers import pipeline

REPO_ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = REPO_ROOT / "OFFLINE-AI-Models" / "smollm2-135m-instruct"


@lru_cache(maxsize=1)
def load_generator():
    return pipeline("text-generation", model=str(MODEL_PATH))


def messages_to_prompt(messages: list[dict[str, str]]) -> str:
    lines = [f"{message['role'].upper()}: {message['content']}" for message in messages]
    return "\n".join([*lines, "ASSISTANT:"])


def call_smolm(messages: list[dict[str, str]], max_new_tokens: int = 40) -> str:
    result = load_generator()(
        messages_to_prompt(messages), max_new_tokens=max_new_tokens, do_sample=False, return_full_text=False
    )
    return result[0]["generated_text"].strip() or "[SmolLM returned no new text]"
