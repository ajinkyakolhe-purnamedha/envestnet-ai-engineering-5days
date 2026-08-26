from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, print_json


def main() -> None:
    history = [{"role": "system", "content": "Answer concisely."}, {"role": "user", "content": "My ticker is AAPL."}]
    first_answer = chat(history, 24)
    history.extend([{"role": "assistant", "content": first_answer}, {"role": "user", "content": "Repeat my ticker."}])
    with_history = chat(history, 24)
    without_history = chat([{"role": "user", "content": "Repeat my ticker."}], 24)
    print_json("Resent history", history)
    print("With history:", with_history)
    print("Without history:", without_history)


if __name__ == "__main__":
    main()
