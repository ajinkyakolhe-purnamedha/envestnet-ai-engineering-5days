"""One concept: a valid MCP read still has a deterministic result limit."""

# The service has three positions, but the model does not need all of them.
positions = [
    {"symbol": "SPY", "value": 48_000},
    {"symbol": "QQQ", "value": 29_000},
    {"symbol": "GLD", "value": 18_000},
]
# Python validates the requested limit before it returns any data.
def show_result(max_positions: int) -> None:
    if max_positions not in {1, 2}:
        print("DENY: max_positions must be 1 or 2")
        return
    # Return only the amount this capability promises to expose.
    result = positions[:max_positions]
    print("Returned positions:", len(result), "of", len(positions))
    print("Truncated for model context:", len(result) < len(positions))
    print("Model facts:", result)


show_result(2)
show_result(3)
