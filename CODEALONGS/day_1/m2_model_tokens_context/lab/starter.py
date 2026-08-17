"""Main lab starter: instrument the M1 assistant without calling a provider."""


def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    """Use the supplied synthetic rates: $0.002/$0.004 per 1,000 tokens."""
    raise NotImplementedError


def trim_history(messages: list[dict[str, str]], keep_turns: int) -> list[dict[str, str]]:
    """Keep recent history without starting on an assistant reply."""
    raise NotImplementedError


def instrument(usage: dict[str, int], cumulative_cost: float) -> dict[str, float]:
    """Return this call's estimate and the updated cumulative total."""
    call_cost = estimate_cost(usage["input_tokens"], usage["output_tokens"])
    return {"call_cost": call_cost, "cumulative_cost": cumulative_cost + call_cost}
