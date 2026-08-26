from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, print_json


def main() -> None:
    instruction = "Answer only from supplied context."
    context = "A diversified portfolio spreads investment across assets."
    question = "What does diversification do?"
    messages = [{"role": "system", "content": instruction}, {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}]
    print_json("Single-turn request", {"instruction": instruction, "context": context, "question": question})
    print("Answer:", chat(messages, 40))


if __name__ == "__main__":
    main()
