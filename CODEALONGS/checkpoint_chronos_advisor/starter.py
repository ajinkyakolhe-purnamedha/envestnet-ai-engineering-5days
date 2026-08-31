"""Build the Chronos checkpoint: chat, evidence, then one tool decision."""

from __future__ import annotations

from collections.abc import Callable

ModelCall = Callable[[list[dict[str, str]]], str]
ALICE_PORTFOLIO = {"client_id": "alice", "cash": 25_000, "holdings": ["SPY", "QQQ", "GLD"]}
POLICY = [
    "No single asset may exceed 35% of the portfolio.",
    "A proposed action must leave at least $2,000 in cash.",
    "Every proposed action requires human confirmation before execution.",
]


def trim_history(history: list[dict[str, str]], max_messages: int = 4) -> list[dict[str, str]]:
    """Stage 1: retain the newest messages only."""
    raise NotImplementedError("Keep only the newest max_messages entries.")


def get_portfolio_summary(client_id: str) -> dict[str, object]:
    if client_id != "alice":
        return {"error": "Client access denied."}
    return ALICE_PORTFOLIO


def search_investment_policy(query: str) -> dict[str, str] | None:
    """Stage 2: return the best matching policy passage, or None."""
    raise NotImplementedError("Rank POLICY passages by their overlapping words.")


def answer_chat(question: str, history: list[dict[str, str]], model_call: ModelCall) -> str:
    messages = [
        {"role": "system", "content": "You are Chronos's educational investor assistant. Use supplied facts only."},
        {"role": "system", "content": f"Trusted portfolio facts: {ALICE_PORTFOLIO}"},
        *trim_history(history),
        {"role": "user", "content": question},
    ]
    return model_call(messages)


def answer_with_evidence(question: str, history: list[dict[str, str]], model_call: ModelCall) -> dict[str, object]:
    evidence = search_investment_policy(question)
    if evidence is None:
        return {"answer": "Not found in the supplied investment policy.", "evidence": None}
    return {"answer": model_call([{ "role": "system", "content": f"Use only this evidence: {evidence['text']}"}, *trim_history(history), {"role": "user", "content": question}]), "evidence": evidence}


def run_agent(question: str, history: list[dict[str, str]], model_call: ModelCall, client_id: str = "alice") -> dict[str, object]:
    """Stage 3: parse one JSON request, validate it, call one tool, then answer."""
    raise NotImplementedError("Use json.loads, an allowlist, and a one-tool trace.")


def main() -> None:
    from m9_memory_verification_hitl.chronos_offline import generate

    print(answer_chat("What do I own?", [], generate))


if __name__ == "__main__":
    main()
