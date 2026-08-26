from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, retrieve


def main() -> None:
    question = "Can Alice raise AAPL to 36 percent?"
    nodes = [{"source": "policy.md#limit", "text": "No single stock allocation may exceed 35 percent."}, {"source": "policy.md#cash", "text": "Cash supports short-term liquidity."}]
    sources = retrieve(question, nodes)
    context = "\n".join(f"[{item['source']}] {item['text']}" for item in sources)
    answer = chat([{"role": "system", "content": "Answer only from context; say unknown if missing."}, {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}], 50)
    print("Sources:", [(item["source"], round(item["score"], 3)) for item in sources])
    print("Grounded answer:", answer)


if __name__ == "__main__":
    main()
