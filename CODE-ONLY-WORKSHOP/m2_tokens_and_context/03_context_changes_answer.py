from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat


def ask(policy: str) -> str:
    return chat([{"role": "system", "content": "Use only the policy."}, {"role": "user", "content": f"Policy: {policy}\nCan Alice hold 36% AAPL?"}], 35)


def main() -> None:
    for policy in ("Single-stock allocation limit: 35%.", "Single-stock allocation limit: 40%."):
        print("Context:", policy)
        print("Answer:", ask(policy))


if __name__ == "__main__":
    main()
