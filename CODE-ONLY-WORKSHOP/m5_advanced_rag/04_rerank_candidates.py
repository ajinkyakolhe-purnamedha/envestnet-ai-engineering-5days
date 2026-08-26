from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, parse_json_object, retrieve


def main() -> None:
    question = "Can AAPL become 36 percent?"
    docs = [{"source": "limit", "text": "No single stock allocation may exceed 35 percent."}, {"source": "risk", "text": "Concentration risk requires explanation."}, {"source": "cash", "text": "Cash supports liquidity."}, {"source": "settlement", "text": "Trades settle after two days."}]
    candidates = retrieve(question, docs, 4)
    print("Dense order:", [item["source"] for item in candidates])
    scored = []
    for item in candidates:
        raw = chat([{"role": "user", "content": f"Return JSON only: {{\"relevance\": 0 to 3}}. Question: {question}\nCandidate: {item['text']}"}], 18)
        value = parse_json_object(raw)
        if value is None or not isinstance(value.get("relevance"), (int, float)):
            print("Invalid reranker output for", item["source"], ":", raw)
            continue
        scored.append({**item, "relevance": float(value["relevance"])})
    print("Reranked valid candidates:", [(item["source"], item["relevance"]) for item in sorted(scored, key=lambda item: item["relevance"], reverse=True)])


if __name__ == "__main__":
    main()
