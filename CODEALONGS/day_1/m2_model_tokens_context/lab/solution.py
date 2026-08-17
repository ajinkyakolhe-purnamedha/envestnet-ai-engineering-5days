"""Instructor solution for the M2 instrumentation lab; no provider I/O."""


def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    return input_tokens / 1_000 * 0.002 + output_tokens / 1_000 * 0.004


def trim_history(messages: list[dict[str, str]], keep_turns: int) -> list[dict[str, str]]:
    retained = messages[-(keep_turns * 2) :]
    while retained and retained[0]["role"] == "assistant":
        retained.pop(0)
    return retained


def instrument(usage: dict[str, int], cumulative_cost: float) -> dict[str, float]:
    call_cost = estimate_cost(usage["input_tokens"], usage["output_tokens"])
    return {"call_cost": call_cost, "cumulative_cost": cumulative_cost + call_cost}
