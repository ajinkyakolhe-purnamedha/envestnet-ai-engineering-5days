"""Shared local Hugging Face setup for M6 snippets."""

from __future__ import annotations

from pathlib import Path

from transformers import AutoModelForCausalLM, AutoTokenizer, GPT2Config


ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = ROOT / "OFFLINE-AI-Models" / "smollm2-135m-instruct"
DATA_DIR = Path(__file__).resolve().parent / "data"
TRAIN_JSONL = DATA_DIR / "support_tickets.jsonl"
EVAL_JSONL = DATA_DIR / "support_eval.jsonl"

SYSTEM_PROMPT = (
    "Classify support tickets. Return only JSON with category and priority."
)


def load_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


def messages_for(row: dict) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": row["input"]},
        {"role": "assistant", "content": row["output"]},
    ]


def prompt_messages_for(row: dict) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": row["input"]},
    ]


def tiny_causal_lm(tokenizer):
    config = GPT2Config(
        vocab_size=len(tokenizer),
        n_positions=128,
        n_embd=32,
        n_layer=1,
        n_head=2,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
    )
    return AutoModelForCausalLM.from_config(config)
