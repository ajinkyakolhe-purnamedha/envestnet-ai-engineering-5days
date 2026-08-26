from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, retrieve, print_json
from llama_index.core.tools import FunctionTool


def price(symbol: str) -> str: return f"{symbol.upper()} price is $182.50"
def policy(question: str) -> str:
    return retrieve(question, [{"source": "policy", "text": "AAPL and every other single-stock allocation may not exceed 35 percent."}], 1)[0]["text"]


def main() -> None:
    price_tool, policy_tool = FunctionTool.from_defaults(fn=price), FunctionTool.from_defaults(fn=policy)
    question = "Can Alice raise AAPL to 36 percent?"
    observations = [str(price_tool.call(symbol="AAPL")), str(policy_tool.call(question=question))]
    answer = chat([{"role": "system", "content": "Answer from tool observations only."}, {"role": "user", "content": f"Question: {question}\nObservations: {observations}"}], 45)
    print_json("Framework-shaped application", {"tools": [price_tool.metadata.name, policy_tool.metadata.name], "max_steps": 2, "observations": observations, "answer": answer})


if __name__ == "__main__":
    main()
