"""Shared data, tools, and offline model call for M7 agentic LLM snippets."""

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
def load_chat_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_path = find_model()
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True).eval()
    return tokenizer, model

def call_smolm(messages: list[dict], max_new_tokens: int = 80) -> str:
    tokenizer, model = load_chat_model()
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(
        **inputs, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tokenizer.eos_token_id)
    new_tokens = output[0, inputs["input_ids"].shape[-1] :]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

QUESTION = "Can Alice raise AAPL to 36% of the portfolio?"

def get_current_price(symbol: str) -> dict:
    prices = {"AAPL": 108.0, "MSFT": 212.5, "GLD": 185.25}
    return {"symbol": symbol.upper(), "price": prices[symbol.upper()]}

def get_portfolio_allocation(client: str, symbol: str) -> dict:
    allocations = {("Alice", "AAPL"): 32.0, ("Alice", "MSFT"): 18.0}
    key = (client, symbol.upper())
    return {"client": client, "symbol": symbol.upper(), "allocation_pct": allocations[key]}

def check_guideline(symbol: str, proposed_allocation_pct: float) -> dict:
    limit_pct = 35.0
    allowed = proposed_allocation_pct <= limit_pct
    return {
        "symbol": symbol.upper(),
        "proposed_allocation_pct": proposed_allocation_pct,
        "limit_pct": limit_pct,
        "allowed": allowed,
    }

TOOL_FUNCTIONS = {
    "get_current_price": get_current_price,
    "get_portfolio_allocation": get_portfolio_allocation,
    "check_guideline": check_guideline,
}

TOOL_SCHEMAS = {
    "get_current_price": {
        "description": "Return current ticker price.",
        "args": {"symbol": "ticker symbol, for example AAPL"},
    },
    "get_portfolio_allocation": {
        "description": "Return current client allocation.",
        "args": {"client": "client name", "symbol": "ticker symbol"},
    },
    "check_guideline": {
        "description": "Check proposed allocation against the 35% limit.",
        "args": {"symbol": "ticker symbol", "proposed_allocation_pct": "proposed percent"},
    },
}

def summarize_guideline(result: dict) -> dict:
    allowed = result["allowed"]
    note = "Allowed. The proposed allocation is within the 35% single-asset limit."
    if not allowed:
        note = "Not allowed. 36% is above the 35% single-asset limit."
    return {"allowed": allowed, "note": note}
