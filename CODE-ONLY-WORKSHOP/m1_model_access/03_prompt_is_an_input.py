from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat


def answer(facts: str) -> str:
    instruction = "Use only supplied facts. Answer in one sentence."
    question = "Can Alice raise AAPL to 36%?"
    prompt = f"Facts:\n{facts}\n\nQuestion: {question}"
    print("Prompt:\n", prompt)
    return chat([{"role": "system", "content": instruction}, {"role": "user", "content": prompt}], 45)


def main() -> None:
    print("35% policy:", answer("The maximum allocation to one stock is 35%."))
    print("40% policy:", answer("The maximum allocation to one stock is 40%."))


if __name__ == "__main__":
    main()
