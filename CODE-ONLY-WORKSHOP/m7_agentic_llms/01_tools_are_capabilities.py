from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, print_json


def get_price(symbol: str) -> dict[str, object]:
    return {"symbol": symbol.upper(), "price": {"AAPL": 182.50, "MSFT": 420.00}.get(symbol.upper())}


def check_limit(symbol: str, proposed_pct: float) -> dict[str, object]:
    return {"symbol": symbol.upper(), "proposed_pct": proposed_pct, "allowed": proposed_pct <= 35}


def main() -> None:
    tools = [{"name": "get_price", "description": "Return a current synthetic price.", "arguments": {"symbol": "ticker"}}, {"name": "check_limit", "description": "Check the 35 percent allocation limit.", "arguments": {"symbol": "ticker", "proposed_pct": "number"}}]
    print_json("Tool registry", tools)
    plan = chat([{"role": "user", "content": f"Available tools: {tools}\nRequest: Can Alice raise AAPL to 36 percent? Explain what tool information you need."}], 55)
    print("Real model planning text:", plan)
    print("Direct Python capability:", get_price("AAPL"), check_limit("AAPL", 36))


if __name__ == "__main__":
    main()
