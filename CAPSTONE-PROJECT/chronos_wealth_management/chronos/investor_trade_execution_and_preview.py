"""Investor trade preview, execution, and history workflows."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.market_data_loading_and_price_queries import (
    get_latest_price_on_or_before_date,
    require_supported_asset,
)
from chronos.api_schemas_investor import TradePreviewResponse, TradeRequest
from chronos.application_database import Account, Holding, Trade
from chronos.application_errors_and_permissions import (
    InsufficientCashError,
    InsufficientSharesError,
)

SHARE_EPSILON = 1e-9


def preview_investor_trade(
    db: Session, account: Account, request: TradeRequest
) -> TradePreviewResponse:
    """Return the point-in-time outcome of a trade without writing any rows."""
    symbol, price, shares = _resolve_trade_at_simulated_price(db, account, request)

    valid = True
    message = f"{request.side} {shares:.4f} shares of {symbol} at ${price:.2f}"

    if request.side == "BUY" and request.amount > account.cash_balance + SHARE_EPSILON:
        valid = False
        message = (
            f"Insufficient cash: buy needs ${request.amount:,.2f} "
            f"but the account has ${account.cash_balance:,.2f}"
        )
    if request.side == "SELL":
        holding = _find_holding(db, account.id, symbol)
        held_shares = holding.shares if holding is not None else 0.0
        if shares > held_shares + SHARE_EPSILON:
            valid = False
            message = (
                f"Insufficient shares: sell needs {shares:.4f} {symbol} "
                f"but the account holds {held_shares:.4f}"
            )

    return TradePreviewResponse(
        symbol=symbol,
        side=request.side,
        amount=request.amount,
        price=price,
        shares=shares,
        simulated_date=account.simulated_date,
        valid=valid,
        message=message,
    )


def execute_investor_trade(
    db: Session, account: Account, request: TradeRequest
) -> Trade:
    """Execute a trade using the account's simulated-date price."""
    symbol, price, shares = _resolve_trade_at_simulated_price(db, account, request)

    if request.side == "BUY":
        _apply_buy(db, account, symbol, shares, price, request.amount)
    else:
        _apply_sell(db, account, symbol, shares, request.amount)

    trade = Trade(
        account_id=account.id,
        symbol=symbol,
        side=request.side,
        shares=shares,
        price=price,
        amount=request.amount,
        simulated_date=account.simulated_date,
    )
    db.add(trade)
    db.flush()
    return trade


def list_trades_for_investor_account(db: Session, account_id: int) -> list[Trade]:
    """Return an investor account's trades in execution order."""
    return list(
        db.scalars(
            select(Trade).where(Trade.account_id == account_id).order_by(Trade.id)
        )
    )


def _resolve_trade_at_simulated_price(
    db: Session, account: Account, request: TradeRequest
) -> tuple[str, float, float]:
    """Normalize a trade symbol and price it once at the account's clock date."""
    symbol = require_supported_asset(db, request.symbol).symbol
    market_price = get_latest_price_on_or_before_date(
        db, symbol, account.simulated_date
    )
    price = market_price.close
    return symbol, price, request.amount / price


def _apply_buy(
    db: Session,
    account: Account,
    symbol: str,
    shares: float,
    price: float,
    amount: float,
) -> None:
    if amount > account.cash_balance + SHARE_EPSILON:
        raise InsufficientCashError(
            f"Buy needs ${amount:,.2f} but the account has "
            f"${account.cash_balance:,.2f}"
        )
    account.cash_balance -= amount

    holding = _find_holding(db, account.id, symbol)
    if holding is None:
        db.add(
            Holding(
                account_id=account.id,
                symbol=symbol,
                shares=shares,
                average_cost=price,
            )
        )
    else:
        total_cost = holding.shares * holding.average_cost + shares * price
        holding.shares += shares
        holding.average_cost = total_cost / holding.shares


def _apply_sell(
    db: Session, account: Account, symbol: str, shares: float, amount: float
) -> None:
    holding = _find_holding(db, account.id, symbol)
    held_shares = holding.shares if holding is not None else 0.0
    if holding is None or shares > held_shares + SHARE_EPSILON:
        raise InsufficientSharesError(
            f"Sell needs {shares:.4f} {symbol} but the account holds "
            f"{held_shares:.4f}"
        )
    account.cash_balance += amount
    holding.shares -= shares
    if holding.shares <= SHARE_EPSILON:
        db.delete(holding)


def _find_holding(db: Session, account_id: int, symbol: str) -> Holding | None:
    return db.scalar(
        select(Holding).where(
            Holding.account_id == account_id, Holding.symbol == symbol
        )
    )
