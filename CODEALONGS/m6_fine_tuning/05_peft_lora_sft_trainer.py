"""One script: fine-tune only LoRA adapter weights with SFTTrainer."""

import sys
import warnings
from pathlib import Path

from datasets import load_dataset
from peft import LoraConfig, PeftModel
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
lora_config = LoraConfig(
    r=4,
    lora_alpha=8,
    task_type="CAUSAL_LM",
    target_modules=["c_attn"],
)
sft_config = SFTConfig(
    output_dir="/tmp/m6-lora-sft-trainer",
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
    peft_config=lora_config,
)

trainable = sum(p.numel() for p in trainer.model.parameters() if p.requires_grad)
total = sum(p.numel() for p in trainer.model.parameters())
trainable_percent = trainable / total * 100

print(type(trainer).__name__)
print("is PEFT model:", isinstance(trainer.model, PeftModel))
print("trainable percent:", round(trainable_percent, 3))
print("dry run: trainer.train() intentionally not called")
