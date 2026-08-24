"""Investor accounts, portfolio valuation, history, and simulation behavior."""

from chronos.investor_accounts.get_investor_account import (
    build_investor_account_response,
    get_account_for_investor_user,
)
from chronos.market_price_queries.get_symbol_price_history import (
    get_symbol_price_history_until_date,
)
from chronos.portfolio_performance.build_account_value_history import (
    build_account_value_history,
)
from chronos.portfolio_performance.calculate_current_portfolio_value import (
    build_current_portfolio_snapshot,
)
from chronos.portfolio_performance.calculate_holding_gain_loss import (
    calculate_holding_cost_basis,
    calculate_holding_market_value,
    calculate_unrealized_gain_loss,
)
from chronos.simulation_clock.advance_simulated_investment_date import (
    advance_simulated_investment_date,
)


def calculate_holding_gain_loss(
    shares: float, average_cost: float, current_price: float
) -> float:
    """Return unrealized gain/loss for a holding at its current price."""
    return calculate_unrealized_gain_loss(
        calculate_holding_market_value(shares, current_price),
        calculate_holding_cost_basis(shares, average_cost),
    )


def get_symbol_price_history(db, symbol, end_date, trading_days: int = 60):
    """Return price rows through the requested simulated date."""
    return get_symbol_price_history_until_date(db, symbol, end_date, trading_days)
