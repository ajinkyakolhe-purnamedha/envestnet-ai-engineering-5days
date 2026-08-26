import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, token_ids, print_json


def main() -> None:
    prompt = "Return a JSON tool request to get the AAPL price."
    started = time.perf_counter()
    output = chat([{"role": "user", "content": prompt}], 30)
    trace = {"model_calls": 1, "tool_calls": 0, "prompt_tokens": len(token_ids(prompt)), "generated_tokens": len(token_ids(output)), "latency_ms": round((time.perf_counter() - started) * 1000), "stop_reason": "one_planning_turn", "raw_output": output}
    print_json("Agent run trace", trace)


if __name__ == "__main__":
    main()
