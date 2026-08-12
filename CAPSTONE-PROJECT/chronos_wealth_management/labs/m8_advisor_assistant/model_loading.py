"""GIVEN: offline SmolLM2 loader — plumbing, not today's lesson.

Finds the committed weights by walking up from this file, loads them as a
transformers pipeline with the hub forced offline, and caches the result.
Returns None when the ``agents`` extra is not installed or anything about
the load fails — your draft function must then fall back to a template.
"""

import os
from functools import cache
from pathlib import Path

_MODEL_DIR_NAME = "smollm2-135m-instruct"
_OFFLINE_MODELS_FOLDER = "OFFLINE-AI-Models"


def find_offline_model_path() -> Path | None:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / _OFFLINE_MODELS_FOLDER / _MODEL_DIR_NAME
        if candidate.is_dir():
            return candidate
    return None


@cache
def load_offline_language_model():
    model_path = find_offline_model_path()
    if model_path is None:
        return None
    try:
        os.environ.setdefault("HF_HUB_OFFLINE", "1")
        os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
        from transformers import pipeline

        return pipeline("text-generation", model=str(model_path))
    except Exception:
        return None
