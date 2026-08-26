import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, retrieve


def lexical(question: str, text: str) -> float:
    words = set(re.findall(r"\w+", question.lower()))
    return len(words & set(re.findall(r"\w+", text.lower()))) / max(len(words), 1)


def main() -> None:
    question = "What is the AAPL concentration limit?"
    docs = [{"source": "limit", "text": "No single stock allocation may exceed 35 percent."}, {"source": "ticker", "text": "AAPL is one security that can create concentration risk."}, {"source": "cash", "text": "Cash supports short-term needs."}]
    dense = {item["source"]: item["score"] for item in retrieve(question, docs, 3)}
    ranked = sorted(({**doc, "dense": dense[doc["source"]], "lexical": lexical(question, doc["text"]), "hybrid": dense[doc["source"]] + lexical(question, doc["text"])} for doc in docs), key=lambda item: item["hybrid"], reverse=True)
    for item in ranked: print(item["source"], {key: round(item[key], 3) for key in ("dense", "lexical", "hybrid")})
    print("Answer:", chat([{"role": "user", "content": f"Context: {ranked[0]['text']}\nQuestion: {question}"}], 35))


if __name__ == "__main__":
    main()
