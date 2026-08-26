from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat


def classify_ticket(text: str) -> str:
    return chat([{"role": "system", "content": "Classify as BILLING or TECHNICAL. Return one label."}, {"role": "user", "content": text}], 12)


def main() -> None:
    print("Raw model label:", classify_ticket("My card was charged twice for the subscription."))


if __name__ == "__main__":
    main()
