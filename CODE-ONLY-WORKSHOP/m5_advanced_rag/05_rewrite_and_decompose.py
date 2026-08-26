from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, parse_json_object, retrieve


def main() -> None:
    question = "Can Alice raise AAPL and what policy is relevant?"
    raw = chat([{"role": "user", "content": f"Return JSON only with rewrite and subquestions (two strings). Question: {question}"}], 60)
    print("Raw transformation:", raw)
    transformed = parse_json_object(raw)
    if transformed is None:
        print("No valid transformation; model output is intentionally not replaced.")
        return
    docs = [{"source": "limit", "text": "No single stock allocation may exceed 35 percent."}, {"source": "risk", "text": "Explain concentration risk before a trade."}]
    queries = [question, str(transformed.get("rewrite", ""))] + [str(item) for item in transformed.get("subquestions", []) if isinstance(item, str)]
    for query in queries:
        print(query, "->", [item["source"] for item in retrieve(query, docs, 2)])


if __name__ == "__main__":
    main()
