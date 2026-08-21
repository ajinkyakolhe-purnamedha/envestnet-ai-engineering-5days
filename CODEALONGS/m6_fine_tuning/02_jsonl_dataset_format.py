"""One script: show the JSONL format used as fine-tuning examples."""

import sys
from pathlib import Path

from datasets import load_dataset

sys.path.insert(0, str(Path(__file__).resolve().parent))

from workshop_hf_setup import TRAIN_JSONL, load_tokenizer, messages_for  # noqa: E402


tokenizer = load_tokenizer()
dataset = load_dataset("json", data_files=str(TRAIN_JSONL), split="train")

row = dataset[0]
messages = messages_for(row)
chat_text = tokenizer.apply_chat_template(messages, tokenize=False)

print(dataset)
print(row)
print(messages)
print(chat_text)
