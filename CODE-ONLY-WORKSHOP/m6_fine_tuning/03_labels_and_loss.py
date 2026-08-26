from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import load_text_model


def main() -> None:
    tokenizer, _ = load_text_model()
    prompt, completion = "Classify: charged twice\nLabel:", " BILLING"
    prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
    input_ids = tokenizer.encode(prompt + completion, add_special_tokens=False)
    labels = [-100] * len(prompt_ids) + input_ids[len(prompt_ids):]
    target = tokenizer.decode([token for token in labels if token != -100])
    print("input_ids:", input_ids)
    print("labels:", labels)
    print("Tokens contributing to loss:", target)


if __name__ == "__main__":
    main()
