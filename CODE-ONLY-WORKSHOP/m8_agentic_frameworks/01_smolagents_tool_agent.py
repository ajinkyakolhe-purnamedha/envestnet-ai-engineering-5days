from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat
from smolagents import tool


@tool
def price_tool(symbol: str) -> str:
    """Return a synthetic market price.

    Args:
        symbol: Ticker symbol, for example AAPL.
    """
    return f"{symbol.upper()} price: $182.50"


def main() -> None:
    plan = chat([{"role": "user", "content": "A tool named price_tool(symbol) is available. State which ticker it should receive for: What is AAPL's price?"}], 32)
    print("Real model planning text:", plan)
    print("smolagents tool name:", price_tool.name)
    print("Framework tool execution:", price_tool.forward(symbol="AAPL"))


if __name__ == "__main__":
    main()
