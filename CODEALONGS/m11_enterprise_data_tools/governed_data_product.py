"""Miniature Chronos service layer used by the M11 code-along.

The function names mirror the real capstone services. The data is small and in
memory so learners can see the MCP pattern before Lab 11 uses Chronos itself.
"""

from __future__ import annotations

from typing import Any


PORTFOLIOS = {
    "alice": {
        "cash_balance": 25_000,
        "holdings": [
            {"symbol": "SPY", "market_value": 48_000},
            {"symbol": "QQQ", "market_value": 29_000},
            {"symbol": "GLD", "market_value": 18_000},
            {"symbol": "BND", "market_value": 12_000},
        ],
    }
}


def build_current_portfolio_snapshot(
    client_id: str, max_positions: int = 3
) -> dict[str, Any]:
    """Return a bounded version of the capstone portfolio-snapshot concept."""
    if max_positions < 1 or max_positions > 3:
        raise ValueError("max_positions must be between 1 and 3")
    portfolio = PORTFOLIOS.get(client_id.lower())
    if portfolio is None:
        return {"status": "not_found", "message": "No portfolio snapshot is available for this client.", "source": "mini_chronos_portfolio_service"}

    holdings = portfolio["holdings"][:max_positions]
    total_value = portfolio["cash_balance"] + sum(
        holding["market_value"] for holding in portfolio["holdings"]
    )
    return {
        "status": "ok", "client_id": client_id.lower(),
        "cash_balance": portfolio["cash_balance"], "total_value": total_value,
        "holdings": holdings, "holding_count_returned": len(holdings),
        "simulated_date": "2026-08-29", "source": "mini_chronos_portfolio_service",
    }


def analyze_client_portfolio(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Calculate a tiny deterministic version of Chronos advisor metrics."""
    holdings = snapshot["holdings"]
    total_value = snapshot["total_value"]
    largest = max(holdings, key=lambda holding: holding["market_value"], default=None)
    largest_percentage = round(largest["market_value"] / total_value * 100, 1) if largest else 0.0
    return {
        "largest_position_symbol": largest["symbol"] if largest else None,
        "largest_position_percentage": largest_percentage,
        "cash_percentage": round(snapshot["cash_balance"] / total_value * 100, 1),
    }


def generate_advisor_review_report(client_id: str) -> dict[str, Any]:
    """Return deterministic internal-review facts, not a model opinion."""
    snapshot = build_current_portfolio_snapshot(client_id)
    if snapshot["status"] != "ok":
        return snapshot
    metrics = analyze_client_portfolio(snapshot)
    recommendations = []
    if metrics["largest_position_percentage"] > 35:
        recommendations.append(
            f"Concentration risk: {metrics['largest_position_symbol']} is "
            f"{metrics['largest_position_percentage']}% of this portfolio."
        )
    return {
        "status": "ok", "client_id": snapshot["client_id"], "metrics": metrics,
        "recommendations": recommendations, "simulated_date": snapshot["simulated_date"],
        "source": "mini_chronos_advisor_service",
    }
