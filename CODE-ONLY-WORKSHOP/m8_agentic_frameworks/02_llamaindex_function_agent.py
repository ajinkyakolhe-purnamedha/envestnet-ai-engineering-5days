from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat
from llama_index.core.tools import FunctionTool


def check_limit(symbol: str, proposed_pct: float) -> str:
    return f"{symbol.upper()} at {proposed_pct}% is {'allowed' if proposed_pct <= 35 else 'not allowed'}"


def main() -> None:
    tool = FunctionTool.from_defaults(fn=check_limit)
    plan = chat([{"role": "user", "content": "A function tool check_limit(symbol, proposed_pct) exists. Explain which arguments to call for AAPL at 36 percent."}], 40)
    print("Real model planning text:", plan)
    print("LlamaIndex tool:", tool.metadata.name)
    print("FunctionTool result:", tool.call(symbol="AAPL", proposed_pct=36.0))


if __name__ == "__main__":
    main()
