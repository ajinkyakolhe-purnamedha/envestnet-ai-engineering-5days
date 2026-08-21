"""Instructor solution for the M2 assistant budgeting lab; no provider I/O."""


def build_messages(
    instruction: str,
    context: str,
    history: list[dict[str, str]],
    new_user_message: str,
) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": instruction},
        *history,
        {"role": "system", "content": f"Context available this turn:\n{context}"},
        {"role": "user", "content": new_user_message},
    ]


def estimate_monthly_cost(one_call_cost: float, calls_per_month: int) -> float:
    return one_call_cost * calls_per_month


def choose_first_model_to_try(rows: list[dict[str, object]]) -> str:
    sorted_rows = sorted(rows, key=lambda row: row["estimated_cost_usd"])
    return str(sorted_rows[0]["tier"])
