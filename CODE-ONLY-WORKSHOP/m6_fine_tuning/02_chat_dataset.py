import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import load_text_model


def main() -> None:
    rows = [{"messages": [{"role": "user", "content": "I was charged twice."}, {"role": "assistant", "content": "BILLING"}]}, {"messages": [{"role": "user", "content": "The app will not open."}, {"role": "assistant", "content": "TECHNICAL"}]}]
    with TemporaryDirectory() as directory:
        path = Path(directory) / "train.jsonl"
        path.write_text("\n".join(json.dumps(row) for row in rows))
        loaded = [json.loads(line) for line in path.read_text().splitlines()]
        tokenizer, _ = load_text_model()
        print("JSONL examples:", len(loaded), "path:", path)
        print("Chat-template text:\n", tokenizer.apply_chat_template(loaded[0]["messages"], tokenize=False))


if __name__ == "__main__":
    main()
