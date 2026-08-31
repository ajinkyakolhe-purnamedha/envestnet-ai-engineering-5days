"""Deterministic checks for the Chronos advisor revision checkpoint."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from checkpoint_chronos_advisor.solution import (
    answer_chat,
    answer_with_evidence,
    get_portfolio_summary,
    run_agent,
    search_investment_policy,
    trim_history,
)


def test_chat_resends_only_four_history_messages() -> None:
    seen: list[list[dict[str, str]]] = []

    def mock_chat(messages: list[dict[str, str]]) -> str:
        seen.append(messages)
        return "Diversification spreads exposure."

    history = [{"role": "user", "content": f"old {number}"} for number in range(6)]

    assert answer_chat("Why diversify?", history, mock_chat) == "Diversification spreads exposure."
    assert len(seen[0]) == 7
    assert "alice" in seen[0][1]["content"]
    assert seen[0][-1]["content"] == "Why diversify?"


def test_portfolio_fixture_denies_other_clients() -> None:
    assert get_portfolio_summary("alice")["client_id"] == "alice"
    assert get_portfolio_summary("bob")["error"] == "Client access denied."
    assert len(trim_history([{"role": "user", "content": "x"}] * 6)) == 4


def test_policy_search_returns_visible_concentration_evidence() -> None:
    evidence = search_investment_policy("What is the concentration limit?")

    assert evidence is not None
    assert "35%" in evidence["text"]


def test_unsupported_policy_question_does_not_call_model() -> None:
    def unexpected_model(messages: list[dict[str, str]]) -> str:
        raise AssertionError("model must not answer without evidence")

    result = answer_with_evidence("What is the estate-planning policy?", [], unexpected_model)

    assert result == {
        "answer": "Not found in the supplied investment policy.",
        "evidence": None,
    }


def test_agent_validates_then_calls_one_portfolio_tool() -> None:
    replies = iter(
        [
            '{"tool": "get_portfolio_summary", "client_id": "alice"}',
            "Alice has $25,000 cash.",
        ]
    )

    result = run_agent("What do I own?", [], lambda _: next(replies))

    assert result["answer"] == "Alice has $25,000 cash."
    assert [item["event"] for item in result["trace"]] == [
        "model_decision",
        "validation",
        "tool_result",
        "final_answer",
    ]


def test_agent_denies_another_client_before_tool_execution() -> None:
    result = run_agent(
        "Show Bob's portfolio",
        [],
        lambda _: '{"tool": "get_portfolio_summary", "client_id": "bob"}',
    )

    assert result["answer"] == "Client access denied."
    assert [item["event"] for item in result["trace"]] == [
        "model_decision",
        "validation",
    ]


def test_agent_rejects_unknown_and_malformed_tool_requests() -> None:
    unknown = run_agent("Trade now", [], lambda _: '{"tool": "place_trade"}')
    malformed = run_agent("Trade now", [], lambda _: "not json")

    assert unknown["answer"] == "Requested tool is not allowed."
    assert malformed["answer"] == "Model returned an invalid tool request."


def test_checkpoint_lab_documents_scope_and_files() -> None:
    root = ROOT / "checkpoint_chronos_advisor"
    readme = (root / "README.md").read_text()

    for phrase in ("Chat", "Evidence", "One-turn agent", "90 minutes", "MCP comes later"):
        assert phrase in readme
    assert (root / "starter.py").exists()
    assert (root / "solution.py").exists()
    assert (root / "hints.md").exists()
    assert "uv run --extra courseware python -m pytest" in readme


def test_checkpoint_solution_stays_small_and_offline_first() -> None:
    source = (ROOT / "checkpoint_chronos_advisor" / "solution.py").read_text()

    assert "m9_memory_verification_hitl.chronos_offline" in source
    assert "mcp" not in source.lower()
    assert "FastAPI" not in source
