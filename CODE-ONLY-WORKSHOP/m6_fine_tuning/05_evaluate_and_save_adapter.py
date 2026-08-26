import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, load_text_model


def main() -> None:
    from peft import LoraConfig, TaskType, get_peft_model

    prompt = "Classify as BILLING or TECHNICAL: I was charged twice."
    baseline = chat([{"role": "user", "content": prompt}], 18)
    _, base = load_text_model()
    adapter = get_peft_model(base, LoraConfig(task_type=TaskType.CAUSAL_LM, r=4, lora_alpha=8, target_modules=["q_proj", "v_proj"]))
    with TemporaryDirectory() as directory:
        root = Path(directory)
        adapter.save_pretrained(root / "adapter")
        (root / "evaluation.json").write_text(json.dumps({"prompt": prompt, "baseline": baseline, "note": "Untrained adapter saved to demonstrate artifact shape."}, indent=2))
        print("Baseline output:", baseline)
        print("Adapter files:", sorted(path.name for path in (root / "adapter").iterdir()))
        print("Evaluation artifact:", root / "evaluation.json")


if __name__ == "__main__":
    main()
