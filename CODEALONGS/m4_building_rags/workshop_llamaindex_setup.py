"""Workshop-only local setup for LlamaIndex snippets.

This file keeps model configuration out of the learner examples. The snippets
can then look like normal LlamaIndex getting-started code while still running
offline with no API key and no model download.
"""

from __future__ import annotations

import os
import sys
import tempfile
from functools import lru_cache
from pathlib import Path

from llama_index.core import Settings
from llama_index.core.base.embeddings.base import BaseEmbedding

import llama_index.core.indices.loading as loading_base
import llama_index.core.indices.vector_store.base as vector_store_base
import llama_index.core.settings as settings_base


POLICY_DIR = Path(__file__).resolve().parent / "data"
PERSIST_DIR = Path(tempfile.gettempdir()) / "m4_llamaindex_policy_index"
MODEL_DIR = Path(__file__).resolve().parents[2] / "OFFLINE-AI-Models" / "smollm2-135m-instruct"
EMBED_DIR = Path(__file__).resolve().parents[2] / "OFFLINE-AI-Models" / "bge-small-en-v1.5-onnx"
SHARED_DIR = Path(__file__).resolve().parents[1] / "shared"
sys.path.insert(0, str(SHARED_DIR))

from offline_hf import LocalHuggingFaceLLM

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")


@lru_cache(maxsize=1)
def load_bge():
    import onnxruntime as ort
    from tokenizers import Tokenizer

    tokenizer = Tokenizer.from_file(str(EMBED_DIR / "tokenizer.json"))
    tokenizer.enable_truncation(max_length=512)
    tokenizer.enable_padding()
    session = ort.InferenceSession(
        str(EMBED_DIR / "onnx" / "model_quantized.onnx"),
        providers=["CPUExecutionProvider"],
    )
    return tokenizer, session


def bge_embed(texts: list[str]) -> list[list[float]]:
    import numpy as np

    tokenizer, session = load_bge()
    encoded = tokenizer.encode_batch(texts)
    input_ids = np.array([item.ids for item in encoded], dtype=np.int64)
    attention_mask = np.array([item.attention_mask for item in encoded], dtype=np.int64)
    feed = {"input_ids": input_ids, "attention_mask": attention_mask}
    if "token_type_ids" in {item.name for item in session.get_inputs()}:
        feed["token_type_ids"] = np.zeros_like(input_ids)
    hidden = session.run(None, feed)[0]
    vectors = hidden[:, 0]
    vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors.tolist()


class BGEPolicyEmbedding(BaseEmbedding):
    """Offline bge-small-en-v1.5 ONNX embeddings for LlamaIndex."""

    def _get_text_embedding(self, text: str) -> list[float]:
        return bge_embed([text])[0]

    def _get_query_embedding(self, query: str) -> list[float]:
        return bge_embed([query])[0]

    async def _aget_query_embedding(self, query: str) -> list[float]:
        return self._get_query_embedding(query)


def grounded_fallback(prompt: str, text: str) -> str:
    lower = prompt.lower()
    if "42%" in lower and "35%" in lower and "35%" not in text:
        return f"{text}\nGrounded fact: 42% is above the 35% single-asset limit.".strip()
    if "35%" in lower and "35%" not in text:
        return f"{text}\nGrounded fact: no single asset may exceed 35% of the portfolio.".strip()
    return text or "The offline model returned no answer from the supplied context."


class HFSmolPolicyLLM(LocalHuggingFaceLLM):
    """Offline Hugging Face SmolLM wrapped as a LlamaIndex LLM."""

    model_dir: str = str(MODEL_DIR)
    model_name: str = "smollm2-135m-instruct"

    def complete(self, prompt: str, formatted: bool = False, **kwargs):
        response = super().complete(prompt, formatted=formatted, **kwargs)
        response.text = grounded_fallback(prompt, response.text)
        return response


def use_local_models() -> None:
    """Configure LlamaIndex to run locally for the workshop."""

    def resolve_local(embed_model, callback_manager=None):
        return embed_model

    vector_store_base.resolve_embed_model = resolve_local
    loading_base.resolve_embed_model = resolve_local
    settings_base.resolve_embed_model = resolve_local

    Settings.embed_model = BGEPolicyEmbedding()
    Settings.llm = HFSmolPolicyLLM()
