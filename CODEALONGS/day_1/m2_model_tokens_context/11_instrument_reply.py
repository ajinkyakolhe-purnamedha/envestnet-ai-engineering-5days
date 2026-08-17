"""One concept: compute a transparent cost estimate from supplied usage data."""


def estimate_cost(
    input_tokens: int, output_tokens: int, input_rate: float, output_rate: float
) -> float:
    """Return a USD estimate when rates are USD per 1,000 tokens."""
    return (input_tokens / 1_000 * input_rate) + (output_tokens / 1_000 * output_rate)


print(f"Estimated cost: ${estimate_cost(200, 50, 0.002, 0.004):.6f}")
