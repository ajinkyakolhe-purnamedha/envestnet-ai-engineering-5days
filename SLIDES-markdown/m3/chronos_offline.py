"""Shared offline helpers for the M3 slide snippets.

No API key, no network. The embedding model is loaded from the repo's
OFFLINE-AI-Models/ folder so the snippets run on the classroom image.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

_HERE = Path(__file__).resolve()
for _parent in _HERE.parents:
    if (_parent / "OFFLINE-AI-Models").is_dir():
        MODELS = _parent / "OFFLINE-AI-Models"
        break
else:  # pragma: no cover
    raise FileNotFoundError("OFFLINE-AI-Models/ not found above " + str(_HERE))

EMBED_MODEL = MODELS / "bge-small-en-v1.5-onnx"


@lru_cache(maxsize=1)
def load_embedder():
    """Return (tokenizer, onnx session) for bge-small."""
    import onnxruntime as ort
    from tokenizers import Tokenizer

    tokenizer = Tokenizer.from_file(str(EMBED_MODEL / "tokenizer.json"))
    tokenizer.enable_truncation(max_length=512)
    tokenizer.enable_padding()
    session = ort.InferenceSession(
        str(EMBED_MODEL / "onnx" / "model_quantized.onnx"),
        providers=["CPUExecutionProvider"],
    )
    return tokenizer, session


def embed(texts: list[str]):
    """Text -> unit vectors. bge uses CLS pooling, then L2 norm."""
    import numpy as np

    tokenizer, session = load_embedder()
    encoded = tokenizer.encode_batch(texts)

    ids = np.array([e.ids for e in encoded], dtype=np.int64)
    mask = np.array([e.attention_mask for e in encoded], dtype=np.int64)
    types = np.zeros_like(ids)

    wanted = {i.name for i in session.get_inputs()}
    feed = {"input_ids": ids, "attention_mask": mask}
    if "token_type_ids" in wanted:
        feed["token_type_ids"] = types

    hidden = session.run(None, feed)[0]
    cls = hidden[:, 0]
    return cls / np.linalg.norm(cls, axis=1, keepdims=True)


def similarity(a, b) -> float:
    """Cosine similarity of two unit vectors."""
    return float(a @ b)
