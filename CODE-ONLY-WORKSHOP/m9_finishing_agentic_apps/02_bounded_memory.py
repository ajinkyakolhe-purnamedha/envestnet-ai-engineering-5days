from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, token_ids, print_json


def main() -> None:
    turns = [{"role": "user", "content": text} for text in ["Alice owns AAPL.", "Her current allocation is 20 percent.", "The limit is 35 percent.", "She asks about increasing it.", "Answer with policy context."]]
    budget, kept, folded = 25, [], []
    for turn in reversed(turns):
        if sum(len(token_ids(item["content"])) for item in kept + [turn]) <= budget: kept.insert(0, turn)
        else: folded.insert(0, turn)
    summary = chat([{"role": "user", "content": f"Summarize these old memory turns in one sentence: {folded}"}], 30) if folded else ""
    print_json("Bounded memory", {"kept": kept, "folded": folded, "model_summary": summary, "stored_trace_count": len(turns)})


if __name__ == "__main__":
    main()
