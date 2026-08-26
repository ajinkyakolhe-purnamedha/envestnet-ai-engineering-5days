from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import load_text_model


def main() -> None:
    import torch
    from peft import LoraConfig, TaskType, get_peft_model

    tokenizer, base = load_text_model()
    adapter = get_peft_model(base, LoraConfig(task_type=TaskType.CAUSAL_LM, r=4, lora_alpha=8, target_modules=["q_proj", "v_proj"]))
    encoded = tokenizer("Classify: charged twice\nLabel: BILLING", return_tensors="pt")
    labels = encoded["input_ids"].clone()
    optimizer = torch.optim.AdamW(adapter.parameters(), lr=1e-4)
    output = adapter(**encoded, labels=labels)
    output.loss.backward()
    optimizer.step()
    trainable = sum(parameter.numel() for parameter in adapter.parameters() if parameter.requires_grad)
    total = sum(parameter.numel() for parameter in adapter.parameters())
    print({"loss": round(float(output.loss.detach()), 4), "trainable": trainable, "total": total})


if __name__ == "__main__":
    main()
