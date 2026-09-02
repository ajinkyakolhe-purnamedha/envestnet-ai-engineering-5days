"""One script: evaluate real base and trained-adapter outputs."""

import json
import sys
from pathlib import Path

from datasets import load_dataset
from peft import PeftModel

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workshop_hf_setup import (  # noqa: E402
    ADAPTER_DIR,
    EVAL_JSONL,
    load_tokenizer,
    prompt_messages_for,
    tiny_causal_lm,
)

FIELDS = {"category", "priority"}

def score_one(reply: str, target: str) -> dict[str, int]:
    try:
        got = json.loads(reply)
    except json.JSONDecodeError:
        return {"parses": 0, "schema": 0, "exact": 0}
    return {
        "parses": 1,
        "schema": int(set(got) == FIELDS),
        "exact": int(got == json.loads(target)),
    }

def summarize(outputs: list[str]) -> dict[str, float]:
    rows = [score_one(output, target) for output, target in zip(outputs, targets)]
    return {metric: sum(row[metric] for row in rows) / len(rows) for metric in rows[0]}


tokenizer = load_tokenizer()
dataset = load_dataset("json", data_files=str(EVAL_JSONL), split="train")
targets = [row["expected"] for row in dataset]


def generate_output(model, row: dict) -> str:
    model.eval()
    prompt = tokenizer.apply_chat_template(
        prompt_messages_for(row), tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=24, do_sample=False)
    return tokenizer.decode(output[0, inputs["input_ids"].shape[-1] :], skip_special_tokens=True)


base_model = tiny_causal_lm(tokenizer)
base_outputs = [generate_output(base_model, row) for row in dataset]
adapter_dir = ADAPTER_DIR
if not adapter_dir.exists():
    raise FileNotFoundError("Run 05_peft_lora_sft_trainer.py before this card.")
adapter_model = PeftModel.from_pretrained(tiny_causal_lm(tokenizer), adapter_dir)
adapter_outputs = [generate_output(adapter_model, row) for row in dataset]
loaded_model = PeftModel.from_pretrained(tiny_causal_lm(tokenizer), adapter_dir)
loaded_outputs = [generate_output(loaded_model, row) for row in dataset]
base_summary = summarize(base_outputs)
adapter_summary = summarize(adapter_outputs)
print("base + prompt:", base_summary)
print("adapter:", adapter_summary)
print("adapter dir:", adapter_dir)
print("base outputs:", base_outputs)
print("adapter outputs:", adapter_outputs)
print("loaded:", type(loaded_model).__name__)
