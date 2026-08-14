"""Shared offline helpers. No API key, no network, ever.

Every model-touching snippet in this folder imports from here so
that the snippet itself stays slide-sized. Weights come from the
repo's OFFLINE-AI-Models/ folder:

    smollm2-135m-instruct   generation  (transformers)
    bge-small-en-v1.5-onnx  embeddings  (onnxruntime)

Nothing here reaches the network. HF_HUB_OFFLINE is set below so a
missing file fails loudly instead of silently downloading.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

# Walk up until we find the model bundle, so a snippet runs from
# SLIDES-markdown/ or any module folder.
_HERE = Path(__file__).resolve()
for _parent in _HERE.parents:
    if (_parent / "OFFLINE-AI-Models").is_dir():
        MODELS = _parent / "OFFLINE-AI-Models"
        break
else:  # pragma: no cover
    raise FileNotFoundError("OFFLINE-AI-Models/ not found above " + str(_HERE))

CHAT_MODEL = MODELS / "smollm2-135m-instruct"
EMBED_MODEL = MODELS / "bge-small-en-v1.5-onnx"
DATA = _HERE.parent / "data"


# --------------------------------------------------------------- chat


@lru_cache(maxsize=1)
def load_chat():
    """Return (tokenizer, model). Cached, so it loads once."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        CHAT_MODEL, local_files_only=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        CHAT_MODEL, local_files_only=True
    ).eval()
    return tokenizer, model


def generate(
    messages: list[dict] | str,
    max_new_tokens: int = 64,
    temperature: float = 0.0,
) -> str:
    """Run SmolLM2 on a chat transcript. Greedy by default.

    A 135M model is small enough to be wrong often. That is on
    purpose -- it makes validation and guardrails feel necessary
    rather than theoretical.
    """
    import torch

    tokenizer, model = load_chat()
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]

    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,
            temperature=temperature or None,
            pad_token_id=tokenizer.eos_token_id,
        )

    new = out[0, inputs["input_ids"].shape[-1]:]
    return tokenizer.decode(new, skip_special_tokens=True).strip()


def count_tokens(text: str) -> int:
    """Exact token count for the model we actually call."""
    tokenizer, _ = load_chat()
    return len(tokenizer.encode(text))


def classify(prompt: str, labels: list[str]) -> str:
    """Pick the likeliest label instead of hoping for one.

    A 135M model cannot reliably be *told* to answer with one
    word. But we can score each candidate answer and take the
    best -- the output space is then closed by construction.
    This is how you get classification out of a small model.
    """
    import torch

    tokenizer, model = load_chat()
    scores = []

    for label in labels:
        messages = [{"role": "user", "content": prompt}]
        head = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        ids = tokenizer(head + label, return_tensors="pt")
        n_head = len(tokenizer(head)["input_ids"])

        with torch.no_grad():
            logits = model(**ids).logits

        logprobs = torch.log_softmax(logits[0, :-1], dim=-1)
        wanted = ids["input_ids"][0, 1:]
        picked = logprobs.gather(1, wanted[:, None])[:, 0]

        # Mean logprob of the label tokens only.
        scores.append(picked[n_head - 1:].mean().item())

    return labels[scores.index(max(scores))]


# ---------------------------------------------------------- embeddings


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
    cls = hidden[:, 0]                       # bge pools on [CLS]
    return cls / np.linalg.norm(cls, axis=1, keepdims=True)


def similarity(a, b) -> float:
    """Cosine similarity of two unit vectors -- just a dot product."""
    return float(a @ b)
