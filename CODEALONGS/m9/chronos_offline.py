"""Tiny offline SmolLM helper for M9 cookbook snippets."""

import os
from functools import lru_cache
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
MODEL_DIR = "smollm2-135m-instruct"

def find_model() -> Path:
    for parent in Path(__file__).resolve().parents:
        model_path = parent / "OFFLINE-AI-Models" / MODEL_DIR
        if model_path.exists():
            return model_path
    raise FileNotFoundError(f"OFFLINE-AI-Models/{MODEL_DIR} not found")

@lru_cache(maxsize=1)
def load_chat():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    model_path = find_model()
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True).eval()
    return tokenizer, model

def to_messages(messages):
    if isinstance(messages, str):
        return [{"role": "user", "content": messages}]
    return messages

def generate(messages, max_new_tokens: int = 64) -> str:
    tokenizer, model = load_chat()
    prompt = tokenizer.apply_chat_template(to_messages(messages), tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(
        **inputs, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tokenizer.eos_token_id
    )
    new_tokens = output[0, inputs["input_ids"].shape[-1] :]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

def count_tokens(text: str) -> int:
    tokenizer, _ = load_chat()
    return len(tokenizer.encode(text))
