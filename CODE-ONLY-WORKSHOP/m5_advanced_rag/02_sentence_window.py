from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, retrieve


def main() -> None:
    sentences = ["Alice owns AAPL in her taxable account.", "No single stock allocation may exceed 35 percent.", "Advisors must explain concentration risk.", "Cash supports short-term liquidity."]
    nodes = [{"sentence": sentence, "text": " ".join(sentences[max(0, i - 1): i + 2])} for i, sentence in enumerate(sentences)]
    winner = retrieve("Can Alice make AAPL 36 percent?", nodes, 1)[0]
    print("Matched sentence:", winner["sentence"])
    print("Window supplied to model:", winner["text"])
    print("Answer:", chat([{"role": "user", "content": f"Context: {winner['text']}\nCan Alice make AAPL 36 percent?"}], 38))


if __name__ == "__main__":
    main()
