"""One concept: Python verifies a deterministic business policy."""


def validate_trade_request(payload: dict[str, object]) -> bool:
    allocation = payload.get("allocation_percent")
    return (
        payload.get("symbol") in {"AAPL", "SPY", "QQQ"}
        and isinstance(allocation, (int, float))
        and allocation <= 35
    )


print(validate_trade_request({"symbol": "AAPL", "allocation_percent": 36}))
