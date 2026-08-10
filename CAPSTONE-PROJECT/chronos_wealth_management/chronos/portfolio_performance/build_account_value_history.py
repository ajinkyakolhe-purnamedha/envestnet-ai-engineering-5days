"""Account value over time, replayed from actual trades.

History never backfills current holdings into the past: a holding contributes
value only from the date its trade actually happened.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.app_startup.seed_demo_users_accounts_and_assets import (
    STARTING_SIMULATED_DATE,
)
from chronos.shared_database.api_schemas import AccountValueHistoryPointResponse
from chronos.shared_database.database_tables import Account, Price, Trade


def build_account_value_history(
    db: Session, account: Account
) -> list[AccountValueHistoryPointResponse]:
    start_date = STARTING_SIMULATED_DATE
    market_dates = [
        row
        for row in db.scalars(
            select(Price.date)
            .where(Price.date >= start_date, Price.date <= account.simulated_date)
            .distinct()
            .order_by(Price.date)
        )
    ]
    trades = list(
        db.scalars(
            select(Trade)
            .where(Trade.account_id == account.id)
            .order_by(Trade.simulated_date, Trade.id)
        )
    )

    cash_balance = account.initial_cash
    shares_by_symbol: dict[str, float] = {}
    next_trade_index = 0
    history: list[AccountValueHistoryPointResponse] = []

    for market_date in market_dates:
        while (
            next_trade_index < len(trades)
            and trades[next_trade_index].simulated_date <= market_date
        ):
            trade = trades[next_trade_index]
            if trade.side == "BUY":
                cash_balance -= trade.amount
                shares_by_symbol[trade.symbol] = (
                    shares_by_symbol.get(trade.symbol, 0.0) + trade.shares
                )
            else:
                cash_balance += trade.amount
                shares_by_symbol[trade.symbol] = (
                    shares_by_symbol.get(trade.symbol, 0.0) - trade.shares
                )
            next_trade_index += 1

        holdings_value = 0.0
        for symbol, shares in shares_by_symbol.items():
            if shares <= 0:
                continue
            close = db.scalar(
                select(Price.close)
                .where(Price.symbol == symbol, Price.date <= market_date)
                .order_by(Price.date.desc())
                .limit(1)
            )
            if close is not None:
                holdings_value += shares * close

        history.append(
            AccountValueHistoryPointResponse(
                date=market_date,
                cash_balance=cash_balance,
                holdings_value=holdings_value,
                total_value=cash_balance + holdings_value,
            )
        )

    return history
