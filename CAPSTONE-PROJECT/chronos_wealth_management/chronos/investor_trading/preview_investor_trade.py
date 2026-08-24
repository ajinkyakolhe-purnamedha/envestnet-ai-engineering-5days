"""Trade preview: price, shares, and validity — writes nothing."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.market_data_loading_and_price_queries import (
    get_latest_price_on_or_before_date,
    require_supported_asset,
)
from chronos.shared_database.api_schemas import TradePreviewResponse, TradeRequest
from chronos.shared_database.database_tables import Account, Holding

SHARE_EPSILON = 1e-9


def preview_investor_trade(
    db: Session, account: Account, request: TradeRequest
) -> TradePreviewResponse:
    symbol = require_supported_asset(db, request.symbol).symbol
    price = get_latest_price_on_or_before_date(db, symbol, account.simulated_date)
    shares = request.amount / price.close

    valid = True
    message = f"{request.side} {shares:.4f} shares of {symbol} at ${price.close:.2f}"

    if request.side == "BUY" and request.amount > account.cash_balance + SHARE_EPSILON:
        valid = False
        message = (
            f"Insufficient cash: buy needs ${request.amount:,.2f} "
            f"but the account has ${account.cash_balance:,.2f}"
        )
    if request.side == "SELL":
        holding = db.scalar(
            select(Holding).where(
                Holding.account_id == account.id, Holding.symbol == symbol
            )
        )
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
        price=price.close,
        shares=shares,
        simulated_date=account.simulated_date,
        valid=valid,
        message=message,
    )
