"""Buy/sell mechanics: cash, holdings, and failure cases.

Fixture prices at the starting simulated date 2020-06-01: AAPL 108, MSFT 196.
"""

import pytest
from sqlalchemy import select

from chronos.investor_trade_execution_and_preview import (
    _resolve_trade_at_simulated_price,
    execute_investor_trade,
    preview_investor_trade,
)
from chronos.api_schemas_investor import TradeRequest
from chronos.application_database import Holding
from chronos.application_errors_and_permissions import (
    InsufficientCashError,
    InsufficientSharesError,
)


def _buy(db, account, amount, symbol="AAPL"):
    return execute_investor_trade(
        db,
        account,
        TradeRequest(user_id=account.user_id, symbol=symbol, side="BUY", amount=amount),
    )


def test_trade_resolution_uses_the_account_simulated_date(db, alice, alice_account):
    symbol, price, shares = _resolve_trade_at_simulated_price(
        db,
        alice_account,
        TradeRequest(user_id=alice.id, symbol="aapl", side="BUY", amount=10_800.0),
    )

    assert symbol == "AAPL"
    assert price == 108.0
    assert shares == pytest.approx(100.0)


def test_buy_reduces_cash_and_creates_holding(db, alice, alice_account):
    trade = _buy(db, alice_account, 10_800.0)
    assert alice_account.cash_balance == pytest.approx(89_200.0)
    assert trade.price == 108.0
    assert trade.shares == pytest.approx(100.0)

    holding = db.scalar(
        select(Holding).where(
            Holding.account_id == alice_account.id, Holding.symbol == "AAPL"
        )
    )
    assert holding is not None
    assert holding.shares == pytest.approx(100.0)
    assert holding.average_cost == pytest.approx(108.0)


def test_sell_reduces_shares_and_increases_cash(db, alice, alice_account):
    _buy(db, alice_account, 10_800.0)
    execute_investor_trade(
        db,
        alice_account,
        TradeRequest(user_id=alice.id, symbol="AAPL", side="SELL", amount=5_400.0),
    )
    assert alice_account.cash_balance == pytest.approx(94_600.0)
    holding = db.scalar(
        select(Holding).where(
            Holding.account_id == alice_account.id, Holding.symbol == "AAPL"
        )
    )
    assert holding.shares == pytest.approx(50.0)


def test_selling_everything_removes_holding(db, alice, alice_account):
    _buy(db, alice_account, 10_800.0)
    execute_investor_trade(
        db,
        alice_account,
        TradeRequest(user_id=alice.id, symbol="AAPL", side="SELL", amount=10_800.0),
    )
    holding = db.scalar(
        select(Holding).where(Holding.account_id == alice_account.id)
    )
    assert holding is None
    assert alice_account.cash_balance == pytest.approx(100_000.0)


def test_buy_with_insufficient_cash_fails(db, alice, alice_account):
    with pytest.raises(InsufficientCashError):
        _buy(db, alice_account, 200_000.0)
    assert alice_account.cash_balance == pytest.approx(100_000.0)


def test_sell_with_insufficient_shares_fails(db, alice, alice_account):
    with pytest.raises(InsufficientSharesError):
        execute_investor_trade(
            db,
            alice_account,
            TradeRequest(user_id=alice.id, symbol="AAPL", side="SELL", amount=1_000.0),
        )


def test_preview_writes_no_rows_and_flags_invalid_trades(db, alice, alice_account):
    preview = preview_investor_trade(
        db,
        alice_account,
        TradeRequest(user_id=alice.id, symbol="AAPL", side="BUY", amount=200_000.0),
    )
    assert preview.valid is False
    assert "Insufficient cash" in preview.message
    assert db.scalar(select(Holding)) is None
    assert alice_account.cash_balance == pytest.approx(100_000.0)


def test_buy_averages_cost_across_dates(db, alice, alice_account):
    from datetime import date

    _buy(db, alice_account, 10_800.0)
    alice_account.simulated_date = date(2020, 6, 8)
    _buy(db, alice_account, 11_000.0)

    holding = db.scalar(
        select(Holding).where(
            Holding.account_id == alice_account.id, Holding.symbol == "AAPL"
        )
    )
    assert holding.shares == pytest.approx(200.0)
    assert holding.average_cost == pytest.approx(109.0)

def test_sell_everything_then_rebuy_uses_fresh_average_cost(db, alice, alice_account):
    from datetime import date

    _buy(db, alice_account, 10_800.0)  # 100 shares at 108
    execute_investor_trade(
        db,
        alice_account,
        TradeRequest(user_id=alice.id, symbol="AAPL", side="SELL", amount=10_800.0),
    )
    alice_account.simulated_date = date(2020, 6, 8)  # AAPL now 110
    _buy(db, alice_account, 11_000.0)

    holding = db.scalar(
        select(Holding).where(
            Holding.account_id == alice_account.id, Holding.symbol == "AAPL"
        )
    )
    assert holding.average_cost == pytest.approx(110.0)


def test_alice_trade_affects_only_the_supported_demo_investor_account(
    db, alice, alice_account
):
    _buy(db, alice_account, 10_800.0)

    assert alice_account.cash_balance == pytest.approx(89_200.0)
    assert db.scalar(select(Holding).where(Holding.account_id == alice_account.id))
