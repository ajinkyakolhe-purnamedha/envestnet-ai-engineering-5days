from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, parse_json_object, print_json


def rule_verdict(allocation_pct: float) -> bool:
    return allocation_pct <= 35


def judge(draft: str) -> dict[str, object] | None:
    raw = chat([{"role": "system", "content": "Return only JSON: {\"pass\": boolean, \"reason\": string, \"evidence\": string}. Policy: allocation must be at most 35 percent."}, {"role": "user", "content": draft}], 55)
    print("Raw judge output:", raw)
    return parse_json_object(raw)


def main() -> None:
    for allocation in (30.0, 36.0):
        draft = f"Propose AAPL allocation of {allocation} percent."
        model_judgment = judge(draft)
        model_pass = model_judgment.get("pass") if isinstance(model_judgment, dict) else None
        print_json("Judge comparison", {"draft": draft, "rule_pass": rule_verdict(allocation), "model_judgment": model_judgment, "agreement": model_pass == rule_verdict(allocation)})


if __name__ == "__main__":
    main()
