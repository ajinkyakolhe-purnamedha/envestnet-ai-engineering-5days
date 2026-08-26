from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, print_json


def route(question: str) -> str: return "portfolio" if "AAPL" in question else "general"
def price() -> dict[str, object]: return {"price": 182.50}
def policy() -> dict[str, object]: return {"limit": 35}
def evaluate(text: str) -> bool: return bool(text.strip())


def main() -> None:
    question = "Can AAPL be 36 percent?"
    with ThreadPoolExecutor(max_workers=2) as pool:
        price_result, policy_result = list(pool.map(lambda fn: fn(), [price, policy]))
    synthesis = chat([{"role": "user", "content": f"Price: {price_result}; policy: {policy_result}; question: {question}. Give a concise answer."}], 45)
    print_json("Controlled workflow", {"route": route(question), "parallel_results": [price_result, policy_result], "synthesis": synthesis, "evaluator_pass": evaluate(synthesis)})


if __name__ == "__main__":
    main()
