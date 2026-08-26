from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, parse_json_object


def main() -> None:
    tools = ["get_price(symbol)", "check_limit(symbol, proposed_pct)"]
    raw = chat([{"role": "system", "content": "Return only JSON: {\"tool\": string, \"arguments\": object}."}, {"role": "user", "content": f"Tools: {tools}. Request a price for AAPL."}], 35)
    action = parse_json_object(raw)
    print("Raw model tool request:", raw)
    if action is None or action.get("tool") not in {"get_price", "check_limit"}:
        print("Rejected action: malformed or unknown tool")
    else:
        print("Parsed action:", action)


if __name__ == "__main__":
    main()
