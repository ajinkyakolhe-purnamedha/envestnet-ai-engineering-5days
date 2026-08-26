from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chunks, print_json


def main() -> None:
    policy = "A portfolio may hold stocks, bonds, and cash. No single stock allocation may exceed 35 percent. Advisors must explain concentration risk before proposing a trade. Cash is available for short-term liquidity needs."
    nodes = [{"chunk_id": index, "source": "policy.md", "text": text} for index, text in enumerate(chunks(policy, size=12, overlap=3), 1)]
    print_json("Document nodes", nodes)


if __name__ == "__main__":
    main()
