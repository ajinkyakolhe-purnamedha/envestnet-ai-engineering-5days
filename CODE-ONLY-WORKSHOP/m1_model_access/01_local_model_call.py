from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, model_path, print_json


def main() -> None:
    messages = [
        {"role": "system", "content": "Answer in one short sentence."},
        {"role": "user", "content": "What is a diversified portfolio?"},
    ]
    print("Local model path:", model_path())
    print_json("Messages sent", messages)
    print("Generated answer:", chat(messages, max_new_tokens=40))


if __name__ == "__main__":
    main()
