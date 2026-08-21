"""One script: send a formatted dataset to TRL's SFTTrainer."""

import sys
import warnings
from pathlib import Path

from datasets import load_dataset
from trl import SFTConfig, SFTTrainer

sys.path.insert(0, str(Path(__file__).resolve().parent))

from workshop_hf_setup import TRAIN_JSONL, load_tokenizer, messages_for, tiny_causal_lm  # noqa: E402


warnings.filterwarnings("ignore", category=UserWarning)

tokenizer = load_tokenizer()
dataset = load_dataset("json", data_files=str(TRAIN_JSONL), split="train[:2]")
dataset = dataset.map(
    lambda row: {"text": tokenizer.apply_chat_template(messages_for(row), tokenize=False)}
)

model = tiny_causal_lm(tokenizer)
sft_config = SFTConfig(
    output_dir="/tmp/m6-sft-trainer",
    max_length=96,
    per_device_train_batch_size=1,
    num_train_epochs=1,
    report_to=[],
    disable_tqdm=True,
    dataset_text_field="text",
)

trainer = SFTTrainer(
    model=model,
    args=sft_config,
    train_dataset=dataset,
    processing_class=tokenizer,
)

print(type(trainer).__name__)
print("rows:", len(trainer.train_dataset))
print("dry run: trainer.train() intentionally not called")
