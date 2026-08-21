"""One script: tokenize fine-tuning text and mask prompt labels."""

import sys
from pathlib import Path

from datasets import load_dataset

sys.path.insert(0, str(Path(__file__).resolve().parent))

from workshop_hf_setup import (  # noqa: E402
    TRAIN_JSONL,
    load_tokenizer,
    messages_for,
    prompt_messages_for,
)


tokenizer = load_tokenizer()
row = load_dataset("json", data_files=str(TRAIN_JSONL), split="train")[0]

prompt_text = tokenizer.apply_chat_template(
    prompt_messages_for(row),
    tokenize=False,
    add_generation_prompt=True,
)
full_text = tokenizer.apply_chat_template(messages_for(row), tokenize=False)

prompt_ids = tokenizer(prompt_text)["input_ids"]
full_ids = tokenizer(full_text)["input_ids"]
labels = [-100] * len(prompt_ids) + full_ids[len(prompt_ids):]

print("input ids:", full_ids[:20])
print("labels:", labels[:20])
print("ignored prompt tokens:", labels.count(-100))
print("learned completion tokens:", len(labels) - labels.count(-100))
