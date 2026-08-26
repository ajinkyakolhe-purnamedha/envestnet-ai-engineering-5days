from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, parse_json_object, print_json


def run_tool(name: str, arguments: dict[str, object]) -> dict[str, object]:
    if name == "get_price" and arguments.get("symbol") == "AAPL": return {"symbol": "AAPL", "price": 182.50}
    if name == "check_limit" and arguments.get("symbol") == "AAPL" and isinstance(arguments.get("proposed_pct"), (int, float)): return {"allowed": float(arguments["proposed_pct"]) <= 35}
    return {"error": "tool or arguments rejected"}


def main() -> None:
    messages = [{"role": "system", "content": "Use JSON actions only: {\"tool\":...,\"arguments\":...}, or {\"final\":...}. Tools: get_price(AAPL), check_limit(AAPL, proposed_pct)."}, {"role": "user", "content": "Can Alice raise AAPL to 36 percent?"}]
    trace, stopped = [], "max_turns"
    for turn in range(1, 4):
        raw = chat(messages, 55)
        action = parse_json_object(raw)
        record = {"turn": turn, "model_output": raw}
        if action is None:
            record["observation"] = "parse_error"; trace.append(record); stopped = "invalid_model_action"; break
        if "final" in action:
            record["final"] = action["final"]; trace.append(record); stopped = "final_answer"; break
        observation = run_tool(str(action.get("tool")), action.get("arguments") if isinstance(action.get("arguments"), dict) else {})
        record["observation"] = observation; trace.append(record)
        messages.extend([{"role": "assistant", "content": raw}, {"role": "tool", "content": str(observation)}])
    print_json("ReAct trace", {"stopped": stopped, "trace": trace})


if __name__ == "__main__":
    main()
