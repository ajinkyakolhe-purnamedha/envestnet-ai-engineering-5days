"""Local LlamaIndex setup owned by the Chronos checkpoint lab."""

from functools import lru_cache
from pathlib import Path

from llama_index.core import Settings
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.llms import CompletionResponse, CustomLLM, LLMMetadata

import llama_index.core.indices.loading as loading_base
import llama_index.core.indices.vector_store.base as vector_store_base
import llama_index.core.settings as settings_base

from offline_model import generate

POLICY_DIR = Path(__file__).resolve().parent / "data"
EMBED_DIR = Path(__file__).resolve().parents[2] / "OFFLINE-AI-Models" / "bge-small-en-v1.5-onnx"


@lru_cache(maxsize=1)
def load_embedding_model():
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


def embed(texts: list[str]) -> list[list[float]]:
    import numpy as np

    tokenizer, session = load_embedding_model()
    encoded = tokenizer.encode_batch(texts)
    input_ids = np.array([item.ids for item in encoded], dtype=np.int64)
    attention_mask = np.array([item.attention_mask for item in encoded], dtype=np.int64)
    feed = {"input_ids": input_ids, "attention_mask": attention_mask}
    if "token_type_ids" in {item.name for item in session.get_inputs()}:
        feed["token_type_ids"] = np.zeros_like(input_ids)
    output = session.run(None, feed)[0]
    vectors = output[:, 0]
    vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors.tolist()


class CheckpointEmbedding(BaseEmbedding):
    """The local BGE embedding model used for Chronos policy retrieval."""

    def _get_text_embedding(self, text: str) -> list[float]:
        return embed([text])[0]

    def _get_query_embedding(self, query: str) -> list[float]:
        return embed([query])[0]

    async def _aget_query_embedding(self, query: str) -> list[float]:
        return self._get_query_embedding(query)


class CheckpointLLM(CustomLLM):
    """A small LlamaIndex wrapper around the checkpoint's real local LLM."""

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(context_window=2048, num_output=64, is_chat_model=True, model_name="smollm2-135m-instruct")

    def complete(self, prompt: str, formatted: bool = False, **kwargs) -> CompletionResponse:
        text = generate([{"role": "user", "content": prompt}], max_new_tokens=64)
        return CompletionResponse(text=text)

    def stream_complete(self, prompt: str, formatted: bool = False, **kwargs):
        yield self.complete(prompt, formatted=formatted, **kwargs)


def use_local_models() -> None:
    """Make LlamaIndex use this checkpoint's offline embedding and LLM."""

    def keep_local(embed_model, callback_manager=None):
        return embed_model

    vector_store_base.resolve_embed_model = keep_local
    loading_base.resolve_embed_model = keep_local
    settings_base.resolve_embed_model = keep_local
    Settings.embed_model = CheckpointEmbedding()
    Settings.llm = CheckpointLLM()
