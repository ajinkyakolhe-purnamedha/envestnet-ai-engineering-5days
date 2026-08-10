"""Deterministic portfolio analysis: metrics, warnings, recommendations."""

from chronos.shared_database.api_schemas import (
    AdvisorMetricResponse,
    PortfolioResponse,
)

CONCENTRATION_THRESHOLD = 0.35
HIGH_CASH_THRESHOLD = 0.40


def analyze_client_portfolio(portfolio: PortfolioResponse) -> AdvisorMetricResponse:
    total_value = portfolio.total_value
    cash_ratio = portfolio.cash_balance / total_value if total_value else 0.0

    largest_position_ratio = 0.0
    largest_position_symbol: str | None = None
    best_holding = None
    worst_holding = None
    for holding in portfolio.holdings:
        position_ratio = holding.market_value / total_value if total_value else 0.0
        if position_ratio > largest_position_ratio:
            largest_position_ratio = position_ratio
            largest_position_symbol = holding.symbol
        if best_holding is None or holding.unrealized_gain_loss > best_holding.unrealized_gain_loss:
            best_holding = holding
        if worst_holding is None or holding.unrealized_gain_loss < worst_holding.unrealized_gain_loss:
            worst_holding = holding

    return AdvisorMetricResponse(
        total_value=total_value,
        cash_ratio=cash_ratio,
        largest_position_ratio=largest_position_ratio,
        largest_position_symbol=largest_position_symbol,
        total_return_percentage=portfolio.total_return_percentage,
        number_of_holdings=len(portfolio.holdings),
        best_holding_symbol=best_holding.symbol if best_holding else None,
        best_holding_gain_loss=(
            best_holding.unrealized_gain_loss if best_holding else None
        ),
        worst_holding_symbol=worst_holding.symbol if worst_holding else None,
        worst_holding_gain_loss=(
            worst_holding.unrealized_gain_loss if worst_holding else None
        ),
    )


def build_advisor_recommendations(portfolio: PortfolioResponse) -> list[str]:
    metrics = analyze_client_portfolio(portfolio)
    recommendations: list[str] = []

    if metrics.largest_position_ratio > CONCENTRATION_THRESHOLD:
        recommendations.append(
            f"Concentration risk: {metrics.largest_position_symbol} is "
            f"{metrics.largest_position_ratio:.0%} of the portfolio "
            f"(threshold {CONCENTRATION_THRESHOLD:.0%})."
        )
    if metrics.cash_ratio > HIGH_CASH_THRESHOLD:
        recommendations.append(
            f"High cash allocation: {metrics.cash_ratio:.0%} of the portfolio "
            f"is cash (threshold {HIGH_CASH_THRESHOLD:.0%})."
        )
    if metrics.number_of_holdings == 1:
        recommendations.append(
            "Low diversification: the portfolio has a single holding."
        )
    if metrics.total_return_percentage < 0:
        recommendations.append(
            f"Performance review: total return is "
            f"{metrics.total_return_percentage:.2f}%."
        )
    if metrics.number_of_holdings == 0:
        recommendations.append(
            "Starting allocation discussion: the portfolio has no holdings yet."
        )

    return recommendations
