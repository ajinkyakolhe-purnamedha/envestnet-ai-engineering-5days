"""Instructor solution: chat, evidence, then one bounded agent decision."""

from __future__ import annotations

from collections.abc import Callable
import json

ModelCall = Callable[[list[dict[str, str]]], str]

ALICE_PORTFOLIO = {
    "client_id": "alice",
    "cash": 25_000,
    "holdings": ["SPY", "QQQ", "GLD"],
}

POLICY = [
    "Concentration limit: no single asset may exceed 35% of the portfolio.",
    "A proposed action must leave at least $2,000 in cash.",
    "Every proposed action requires human confirmation before execution.",
]

def trim_history(
    history: list[dict[str, str]], max_messages: int = 4
) -> list[dict[str, str]]:
    """Keep the newest display turns in the model transcript."""
    return history[-max_messages:]


def get_portfolio_summary(client_id: str) -> dict[str, object]:
    """Return the one educational portfolio this lab permits."""
    if client_id != "alice":
        return {"error": "Client access denied."}
    return ALICE_PORTFOLIO


def search_investment_policy(query: str) -> dict[str, str] | None:
    """Find one visible policy passage with a deliberately tiny retriever."""
    stop_words = {"what", "is", "the", "a", "an", "of", "does", "about", "policy"}
    words = set(query.lower().replace("?", "").split()) - stop_words
    ranked = sorted(
        POLICY,
        key=lambda text: len(
            words & set(text.lower().replace("%", "").replace(".", "").split())
        ),
        reverse=True,
    )
    best_words = set(ranked[0].lower().replace("%", "").replace(".", "").split())
    if not words & best_words:
        return None
    return {"source": "mini_policy.md", "text": ranked[0]}


def answer_chat(
    question: str, history: list[dict[str, str]], model_call: ModelCall
) -> str:
    """Answer using Alice's trusted facts and bounded chat context."""
    messages = [
        {
            "role": "system",
            "content": "You are Chronos's educational investor assistant. Use supplied facts only.",
        },
        {"role": "system", "content": f"Trusted portfolio facts: {ALICE_PORTFOLIO}"},
        *trim_history(history),
        {"role": "user", "content": question},
    ]
    return model_call(messages)


def answer_with_evidence(
    question: str, history: list[dict[str, str]], model_call: ModelCall
) -> dict[str, object]:
    """Answer a policy question only when a policy passage was found."""
    evidence = search_investment_policy(question)
    if evidence is None:
        return {"answer": "Not found in the supplied investment policy.", "evidence": None}
    messages = [
        {"role": "system", "content": f"Use only this evidence: {evidence['text']}"},
        *trim_history(history),
        {"role": "user", "content": question},
    ]
    return {"answer": model_call(messages), "evidence": evidence}


def run_agent(
    question: str,
    history: list[dict[str, str]],
    model_call: ModelCall,
    client_id: str = "alice",
) -> dict[str, object]:
    """Let the model choose one allowed read-only tool, then answer."""
    decision = model_call(
        [
            {
                "role": "system",
                "content": (
                    'Return JSON only. Choose either '
                    '{"tool":"get_portfolio_summary","client_id":"alice"} '
                    'or {"tool":"search_investment_policy","query":"..."}.'
                ),
            },
            {"role": "user", "content": question},
        ]
    )
    trace: list[dict[str, object]] = [{"event": "model_decision", "text": decision}]
    try:
        request = json.loads(decision)
    except json.JSONDecodeError:
        return {"answer": "Model returned an invalid tool request.", "trace": trace}

    if request.get("tool") == "get_portfolio_summary" and request.get("client_id") == client_id == "alice":
        result: dict[str, object] | None = get_portfolio_summary("alice")
    elif request.get("tool") == "search_investment_policy" and isinstance(request.get("query"), str):
        result = search_investment_policy(request["query"])
    elif request.get("tool") == "get_portfolio_summary":
        return {
            "answer": "Client access denied.",
            "trace": [*trace, {"event": "validation", "allowed": False}],
        }
    else:
        return {
            "answer": "Requested tool is not allowed.",
            "trace": [*trace, {"event": "validation", "allowed": False}],
        }

    trace.extend(
        [
            {"event": "validation", "allowed": True},
            {"event": "tool_result", "result": result},
        ]
    )
    if result is None:
        answer = "Not found in the supplied investment policy."
    else:
        answer = model_call(
            [
                {
                    "role": "system",
                    "content": f"Answer educationally from this tool result only: {result}",
                },
                {"role": "user", "content": question},
            ]
        )
    trace.append({"event": "final_answer", "text": answer})
    return {"answer": answer, "trace": trace}


def main() -> None:
    from m9_memory_verification_hitl.chronos_offline import generate

    result = run_agent("What does the policy say about concentration risk?", [], generate)
    print("Answer:", result["answer"])
    print("Trace:")
    for event in result["trace"]:
        print(event)


if __name__ == "__main__":
    main()
