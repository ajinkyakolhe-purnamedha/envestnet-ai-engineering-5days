"""GIVEN: offline SmolLM2 loader for the Day 1 preview labs."""

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
