from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, parse_json_object, print_json


def get_price(symbol: str) -> dict[str, object]: return {"symbol": symbol.upper(), "price": 182.50}
def check_limit(symbol: str, proposed_pct: float) -> dict[str, object]: return {"symbol": symbol.upper(), "allowed": proposed_pct <= 35}


def dispatch(action: dict[str, object]) -> dict[str, object]:
    name, args = action.get("tool"), action.get("arguments")
    if name not in {"get_price", "check_limit"} or not isinstance(args, dict): return {"error": "unknown tool or invalid arguments"}
    if name == "get_price" and isinstance(args.get("symbol"), str): return get_price(args["symbol"])
    if name == "check_limit" and isinstance(args.get("symbol"), str) and isinstance(args.get("proposed_pct"), (int, float)): return check_limit(args["symbol"], float(args["proposed_pct"]))
    return {"error": "schema validation failed"}


def main() -> None:
    raw = chat([{"role": "user", "content": "Return only JSON {'tool':'check_limit','arguments':{'symbol':'AAPL','proposed_pct':36}} using double quotes."}], 38)
    action = parse_json_object(raw)
    print("Raw model request:", raw)
    print_json("Python observation", dispatch(action or {}))


if __name__ == "__main__":
    main()
