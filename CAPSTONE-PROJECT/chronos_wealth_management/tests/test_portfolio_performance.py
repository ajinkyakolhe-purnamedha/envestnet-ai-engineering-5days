"""Portfolio valuation at simulated-date prices; honest account history."""

from datetime import date

import pytest

from chronos.investor_trade_execution_and_preview import execute_investor_trade
from chronos.investor_accounts_portfolios_and_history import (
    build_account_value_history,
    build_current_portfolio_snapshot,
    calculate_holding_cost_basis,
    calculate_holding_market_value,
    calculate_unrealized_gain_loss,
)
from chronos.api_schemas_investor import TradeRequest


def test_arithmetic_helpers():
    assert calculate_holding_market_value(10, 110.0) == 1_100.0
    assert calculate_holding_cost_basis(10, 100.0) == 1_000.0
    assert calculate_unrealized_gain_loss(1_100.0, 1_000.0) == 100.0


def test_portfolio_valuation_uses_simulated_date_prices(db, alice, alice_account):
    execute_investor_trade(
        db,
        alice_account,
        TradeRequest(user_id=alice.id, symbol="AAPL", side="BUY", amount=10_800.0),
    )
    alice_account.simulated_date = date(2020, 6, 8)  # AAPL close moves 108 -> 110

    portfolio = build_current_portfolio_snapshot(db, alice_account)
    holding = portfolio.holdings[0]
    assert holding.current_price == 110.0
    assert holding.market_value == pytest.approx(11_000.0)
    assert holding.unrealized_gain_loss == pytest.approx(200.0)
    assert portfolio.total_value == pytest.approx(89_200.0 + 11_000.0)
    assert portfolio.total_return_amount == pytest.approx(200.0)
    assert portfolio.total_return_percentage == pytest.approx(0.2)


def test_allocation_percentages_sum_with_cash(db, alice, alice_account):
    execute_investor_trade(
        db,
        alice_account,
        TradeRequest(user_id=alice.id, symbol="AAPL", side="BUY", amount=50_000.0),
    )
    portfolio = build_current_portfolio_snapshot(db, alice_account)
    assert portfolio.holdings[0].allocation_percentage == pytest.approx(50.0)


def test_account_history_does_not_backfill_current_holdings(db, alice, alice_account):
    alice_account.simulated_date = date(2020, 6, 8)
    execute_investor_trade(
        db,
        alice_account,
        TradeRequest(user_id=alice.id, symbol="AAPL", side="BUY", amount=11_000.0),
    )
    alice_account.simulated_date = date(2020, 6, 15)

    history = build_account_value_history(db, alice_account)
    points_by_date = {point.date: point for point in history}

    before_trade = points_by_date[date(2020, 6, 1)]
    assert before_trade.holdings_value == 0.0
    assert before_trade.total_value == pytest.approx(100_000.0)

    on_trade_date = points_by_date[date(2020, 6, 8)]
    assert on_trade_date.holdings_value == pytest.approx(11_000.0)
    assert on_trade_date.cash_balance == pytest.approx(89_000.0)

    after_trade = points_by_date[date(2020, 6, 15)]
    assert after_trade.holdings_value == pytest.approx(11_200.0)  # AAPL 112


def test_history_stops_at_simulated_date(db, alice, alice_account):
    history = build_account_value_history(db, alice_account)
    assert history
    assert max(point.date for point in history) <= alice_account.simulated_date
