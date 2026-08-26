from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, print_json


def main() -> None:
    history = [{"role": "system", "content": "Answer concisely."}, {"role": "user", "content": "My ticker is AAPL."}]
    first = chat(history, 20)
    history.extend([{"role": "assistant", "content": first}, {"role": "user", "content": "Repeat my ticker."}])
    with_memory = chat(history, 20)
    without_memory = chat([{"role": "user", "content": "Repeat my ticker."}], 20)
    print_json("Memory comparison", {"history": history, "with_memory": with_memory, "without_memory": without_memory})


if __name__ == "__main__":
    main()
