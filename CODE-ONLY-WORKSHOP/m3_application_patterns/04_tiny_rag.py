from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, retrieve


def main() -> None:
    question = "May Alice raise AAPL to 36 percent?"
    documents = [{"source": "policy.md", "text": "No single stock allocation may exceed 35 percent."}, {"source": "faq.md", "text": "Deposits settle after two business days."}, {"source": "guide.md", "text": "Diversification reduces concentration risk."}]
    source = retrieve(question, documents, 1)[0]
    print("Retrieved source:", source["source"], round(source["score"], 3))
    print("Answer:", chat([{"role": "system", "content": "Answer only from context; say unknown otherwise."}, {"role": "user", "content": f"Context: {source['text']}\nQuestion: {question}"}], 40))


if __name__ == "__main__":
    main()
