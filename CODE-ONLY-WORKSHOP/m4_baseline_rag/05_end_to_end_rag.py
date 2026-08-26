from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, chunks, retrieve, print_json


def run(question: str) -> dict[str, object]:
    document = "No single stock allocation may exceed 35 percent. Cash supports liquidity. Diversification reduces concentration risk."
    nodes = [{"source": "policy.md", "text": text} for text in chunks(document, 10, 2)]
    sources = retrieve(question, nodes)
    context = "\n".join(item["text"] for item in sources)
    answer = chat([{"role": "system", "content": "Use only context; say unknown if context does not answer."}, {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}], 45)
    return {"question": question, "sources": sources, "answer": answer}


def main() -> None:
    print_json("Answerable trace", run("What is the stock limit?"))
    print_json("Missing-answer trace", run("What is the client's birthday?"))


if __name__ == "__main__":
    main()
