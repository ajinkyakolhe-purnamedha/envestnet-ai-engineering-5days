from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, model_path, token_ids


def main() -> None:
    prompt = "Classify this support ticket as BILLING or TECHNICAL: I was charged twice."
    print("Base model:", model_path())
    print("Prompt tokens:", len(token_ids(prompt)))
    print("Baseline output:", chat([{"role": "user", "content": prompt}], 24))


if __name__ == "__main__":
    main()
