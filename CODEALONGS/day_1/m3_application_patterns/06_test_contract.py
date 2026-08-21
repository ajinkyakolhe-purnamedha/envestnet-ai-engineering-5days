"""One concept: Python verifies a deterministic business policy.

Try:
- Test an allowed symbol at 35%.
- Test an unknown symbol.
- Explain why an LLM should not be the final judge of a numeric limit.
"""


def validate_trade_request(payload: dict[str, object]) -> bool:
    allocation = payload.get("allocation_percent")
    return (
        payload.get("symbol") in {"AAPL", "SPY", "QQQ"}
        and isinstance(allocation, (int, float))
        and allocation <= 35
    )


examples = [
    {"symbol": "AAPL", "allocation_percent": 36},
    {"symbol": "SPY", "allocation_percent": 35},
    {"symbol": "UNKNOWN", "allocation_percent": 20},
]
results = [validate_trade_request(example) for example in examples]

for example, result in zip(examples, results):
    print(example, "allowed:", result)
