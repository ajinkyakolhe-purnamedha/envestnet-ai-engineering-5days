"""Trade execution: moves cash, updates holdings, records the trade."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.market_data_loading_and_price_queries import (
    get_latest_price_on_or_before_date,
    require_supported_asset,
)
from chronos.shared_database.api_schemas import TradeRequest
from chronos.shared_database.database_tables import Account, Holding, Trade
from chronos.shared_database.domain_errors import (
    InsufficientCashError,
    InsufficientSharesError,
)

SHARE_EPSILON = 1e-9


def execute_investor_trade(
    db: Session, account: Account, request: TradeRequest
) -> Trade:
    symbol = require_supported_asset(db, request.symbol).symbol
    price = get_latest_price_on_or_before_date(db, symbol, account.simulated_date)
    shares = request.amount / price.close

    if request.side == "BUY":
        _apply_buy(db, account, symbol, shares, price.close, request.amount)
    else:
        _apply_sell(db, account, symbol, shares, request.amount)

    trade = Trade(
        account_id=account.id,
        symbol=symbol,
        side=request.side,
        shares=shares,
        price=price.close,
        amount=request.amount,
        simulated_date=account.simulated_date,
    )
    db.add(trade)
    db.flush()
    return trade


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
