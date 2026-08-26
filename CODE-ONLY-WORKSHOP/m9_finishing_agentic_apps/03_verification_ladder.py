from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, parse_json_object, print_json


def rules(request: dict[str, object] | None) -> dict[str, bool]:
    return {"has_ticker": isinstance(request, dict) and isinstance(request.get("ticker"), str), "numeric_allocation": isinstance(request, dict) and isinstance(request.get("allocation_pct"), (int, float)), "within_35_percent": isinstance(request, dict) and isinstance(request.get("allocation_pct"), (int, float)) and float(request["allocation_pct"]) <= 35}


def main() -> None:
    raw = chat([{"role": "user", "content": "Return only JSON with ticker and allocation_pct for: Raise AAPL to 36 percent."}], 35)
    request = parse_json_object(raw)
    result = rules(request)
    print_json("Verification ladder", {"raw_model_draft": raw, "parsed": request, "rules": result, "verified": all(result.values())})


if __name__ == "__main__":
    main()
