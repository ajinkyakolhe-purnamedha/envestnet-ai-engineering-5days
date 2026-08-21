"""One script: evaluate outputs and save/load a LoRA adapter."""

import json
import sys
import tempfile
from pathlib import Path

from peft import LoraConfig, PeftModel, get_peft_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workshop_hf_setup import load_tokenizer, tiny_causal_lm  # noqa: E402

FIELDS = {"category", "priority"}
targets = [
    '{"category":"access","priority":"high"}',
    '{"category":"product_bug","priority":"medium"}',
    '{"category":"how_to","priority":"low"}',
]
base_outputs = [
    "This is an urgent access issue.",
    '{"type":"product_bug","severity":"medium"}',
    targets[2],
]
adapter_outputs = targets

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


base_summary = summarize(base_outputs)
adapter_summary = summarize(adapter_outputs)
tokenizer = load_tokenizer()
base_model = tiny_causal_lm(tokenizer)
lora_config = LoraConfig(r=4, lora_alpha=8, task_type="CAUSAL_LM", target_modules=["c_attn"])
adapter_model = get_peft_model(base_model, lora_config)
adapter_dir = Path(tempfile.mkdtemp(prefix="m6-support-ticket-adapter-"))
adapter_model.save_pretrained(adapter_dir)
loaded_model = PeftModel.from_pretrained(tiny_causal_lm(tokenizer), adapter_dir)
print("base + prompt:", base_summary)
print("adapter:", adapter_summary)
print("adapter dir:", adapter_dir)
print("loaded:", type(loaded_model).__name__)
