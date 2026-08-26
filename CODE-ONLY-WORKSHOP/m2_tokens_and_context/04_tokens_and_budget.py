from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import token_ids


def main() -> None:
    history = ["What is diversification?", "It spreads risk across assets.", "Give an example.", "A mix of stocks and bonds."]
    budget, total = 24, 0
    for turn in history:
        ids = token_ids(turn)
        total += len(ids)
        print({"text": turn, "token_ids": ids, "running_tokens": total, "within_budget": total <= budget})
    input_tokens, output_tokens = total, 30
    print("Illustrative cost at $0.20/M input and $0.80/M output:", (input_tokens * 0.20 + output_tokens * 0.80) / 1_000_000)


if __name__ == "__main__":
    main()
