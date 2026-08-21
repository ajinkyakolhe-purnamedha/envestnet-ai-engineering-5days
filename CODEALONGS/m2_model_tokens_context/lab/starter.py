"""Main lab starter: inspect and budget a multi-turn assistant offline."""


def build_messages(
    instruction: str,
    context: str,
    history: list[dict[str, str]],
    new_user_message: str,
) -> list[dict[str, str]]:
    """Assemble the exact messages sent to the model on this turn."""
    raise NotImplementedError


def estimate_monthly_cost(one_call_cost: float, calls_per_month: int) -> float:
    """Project one-call cost to a monthly operating estimate."""
    raise NotImplementedError


def choose_first_model_to_try(rows: list[dict[str, object]]) -> str:
    """Return the lowest-cost tier name unless the task evidence justifies more."""
    raise NotImplementedError
