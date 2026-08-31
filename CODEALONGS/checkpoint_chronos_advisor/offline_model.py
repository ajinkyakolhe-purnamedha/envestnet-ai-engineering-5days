"""Small local SmolLM helper used only by the Chronos checkpoint lab."""

from functools import lru_cache
from pathlib import Path


MODEL_DIR = Path(__file__).resolve().parents[2] / "OFFLINE-AI-Models" / "smollm2-135m-instruct"


@lru_cache(maxsize=1)
def load_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, local_files_only=True).eval()
    return tokenizer, model


def generate(messages: list[dict[str, str]], max_new_tokens: int = 80) -> str:
    """Generate one deterministic reply from the local 135M model."""
    tokenizer, model = load_model()
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
    )
    new_tokens = output[0, inputs["input_ids"].shape[-1] :]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
