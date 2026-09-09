"""The real, offline model boundary shared by the three draft modules."""

from __future__ import annotations

import sys
import time
from pathlib import Path

draft_root = Path(__file__).resolve().parents[1]
repository_root = draft_root.parent
codealongs_root = repository_root / "CODEALONGS"
sys.path.insert(0, str(codealongs_root / "shared"))

from offline_hf import generate_chat  # noqa: E402

model_dir = repository_root / "OFFLINE-AI-Models" / "smollm2-135m-instruct"


def call_local_model(messages: list[dict[str, str]], max_new_tokens: int = 64) -> dict[str, object]:
    """Run the pre-downloaded model for real, or report its explicit failure."""

    started_at = time.perf_counter()
    try:
        text = generate_chat(str(model_dir), messages, max_new_tokens=max_new_tokens)
    except Exception as error:  # A missing local model must never look like a success.
        return {
            "status": "local_model_unavailable",
            "backend": "local Hugging Face inference",
            "model": model_dir.name,
            "latency_ms": round((time.perf_counter() - started_at) * 1_000, 1),
            "error": f"{type(error).__name__}: {error}",
        }
    return {
        "status": "complete",
        "backend": "local Hugging Face inference",
        "model": model_dir.name,
        "latency_ms": round((time.perf_counter() - started_at) * 1_000, 1),
        "text": text,
    }
