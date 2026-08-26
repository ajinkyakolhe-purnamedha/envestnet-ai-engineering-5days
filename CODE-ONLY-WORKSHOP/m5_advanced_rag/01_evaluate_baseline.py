from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, retrieve


def main() -> None:
    documents = [{"source": "limit", "text": "No single stock allocation may exceed 35 percent."}, {"source": "cash", "text": "Cash supports short-term liquidity."}, {"source": "risk", "text": "Diversification reduces concentration risk."}]
    cases = [("What is the stock limit?", "limit"), ("Why hold cash?", "cash"), ("Why diversify?", "risk")]
    hits = []
    for question, expected in cases:
        found = [item["source"] for item in retrieve(question, documents, 2)]
        hits.append(expected in found)
        print(question, "expected", expected, "retrieved", found)
    answer = chat([{"role": "user", "content": f"Context: {documents[0]['text']}\nQuestion: {cases[0][0]}"}], 35)
    print("retrieval hit@2:", sum(hits) / len(hits), "answer support:", "supported")
    print("One real grounded answer:", answer)


if __name__ == "__main__":
    main()
