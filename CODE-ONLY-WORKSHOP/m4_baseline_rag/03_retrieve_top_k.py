from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import retrieve


def main() -> None:
    nodes = [{"source": "policy.md#limit", "text": "No single stock allocation may exceed 35 percent."}, {"source": "policy.md#cash", "text": "Cash supports short-term liquidity."}, {"source": "policy.md#risk", "text": "Concentration risk rises when one holding dominates."}]
    for rank, node in enumerate(retrieve("Can AAPL be 36 percent?", nodes, top_k=2), 1):
        print(rank, node["source"], round(node["score"], 3), node["text"])


if __name__ == "__main__":
    main()
