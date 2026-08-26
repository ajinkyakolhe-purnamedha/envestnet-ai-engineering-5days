from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, retrieve


def main() -> None:
    question = "How much can one stock occupy?"
    documents = [
        {"source": "policy", "text": "A single stock cannot exceed 35 percent of a portfolio."},
        {"source": "diversification", "text": "Investors spread money across several assets."},
        {"source": "cash", "text": "Cash can provide liquidity for short-term needs."},
    ]
    ranked = retrieve(question, documents, top_k=3)
    for item in ranked:
        print(item["source"], round(item["score"], 3), item["text"])
    winner = ranked[0]
    print("Grounded answer:", chat([{"role": "user", "content": f"Context: {winner['text']}\nQuestion: {question}"}], 40))


if __name__ == "__main__":
    main()
