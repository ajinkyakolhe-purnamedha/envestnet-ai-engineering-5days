from __future__ import annotations

import json
import math
import os
import re
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Any


def repo_root() -> Path:
    roots = [Path(__file__).resolve().parents[1]]
    try:
        common_git_dir = subprocess.check_output(
            ["git", "rev-parse", "--git-common-dir"], text=True
        ).strip()
        roots.append(Path(common_git_dir).resolve().parent)
    except (OSError, subprocess.CalledProcessError):
        pass
    return next(root for root in roots if (root / "OFFLINE-AI-Models").exists())


def model_path(name: str = "smollm") -> Path:
    configured = os.getenv("COURSEWARE_MODEL_DIR")
    if configured and Path(configured).is_dir():
        return Path(configured)
    folder = {
        "smollm": "smollm2-135m-instruct",
        "bge": "bge-small-en-v1.5-onnx",
    }[name]
    path = repo_root() / "OFFLINE-AI-Models" / folder
    if not path.is_dir():
        raise FileNotFoundError(f"Expected local model files at {path}")
    return path


@lru_cache(maxsize=1)
def load_text_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    path = model_path("smollm")
    tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(path, local_files_only=True).eval()
    return tokenizer, model


def chat(messages: list[dict[str, str]], max_new_tokens: int = 80) -> str:
    """Run genuine local generation; this function never creates a substitute reply."""
    tokenizer, model = load_text_model()
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt"
    ).to(model.device)
    output = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.decode(output[0][inputs["input_ids"].shape[-1] :], skip_special_tokens=True).strip()


def token_ids(text: str) -> list[int]:
    tokenizer, _ = load_text_model()
    return tokenizer.encode(text, add_special_tokens=False)


@lru_cache(maxsize=1)
def load_embedding_model():
    import onnxruntime as ort
    from tokenizers import Tokenizer

    path = model_path("bge")
    tokenizer = Tokenizer.from_file(str(path / "tokenizer.json"))
    tokenizer.enable_truncation(max_length=256)
    tokenizer.enable_padding()
    session = ort.InferenceSession(
        str(path / "onnx" / "model_quantized.onnx"), providers=["CPUExecutionProvider"]
    )
    return tokenizer, session


def embed(text: str) -> list[float]:
    """Run genuine local BGE ONNX inference and return its normalized CLS vector."""
    import numpy as np

    tokenizer, session = load_embedding_model()
    encoded = tokenizer.encode(text)
    input_ids = np.array([encoded.ids], dtype=np.int64)
    attention_mask = np.array([encoded.attention_mask], dtype=np.int64)
    feed = {"input_ids": input_ids, "attention_mask": attention_mask}
    if "token_type_ids" in {item.name for item in session.get_inputs()}:
        feed["token_type_ids"] = np.zeros_like(input_ids)
    hidden = session.run(None, feed)[0][0, 0]
    return (hidden / np.linalg.norm(hidden)).tolist()


def cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right)) / math.sqrt(
        sum(a * a for a in left) * sum(b * b for b in right)
    )


def parse_json_object(text: str) -> dict[str, Any] | None:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        value = json.loads(match.group())
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def print_json(label: str, value: Any) -> None:
    print(f"\n{label}:")
    print(json.dumps(value, indent=2, default=str))


def chunks(text: str, size: int = 18, overlap: int = 4) -> list[str]:
    words = text.split()
    step = size - overlap
    return [" ".join(words[start : start + size]) for start in range(0, len(words), step)]


def retrieve(question: str, documents: list[dict[str, str]], top_k: int = 2) -> list[dict[str, Any]]:
    question_vector = embed(question)
    ranked = [
        {**document, "score": cosine(question_vector, embed(document["text"]))}
        for document in documents
    ]
    return sorted(ranked, key=lambda item: item["score"], reverse=True)[:top_k]
