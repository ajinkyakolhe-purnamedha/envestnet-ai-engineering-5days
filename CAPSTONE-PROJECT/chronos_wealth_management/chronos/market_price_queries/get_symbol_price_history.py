"""Historical close prices for a symbol, never past the simulated date."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.shared_database.database_tables import Price


def get_symbol_price_history_until_date(
    db: Session, symbol: str, end_date: date, trading_days: int = 60
) -> list[Price]:
    recent_prices = list(
        db.scalars(
            select(Price)
            .where(Price.symbol == symbol, Price.date <= end_date)
            .order_by(Price.date.desc())
            .limit(trading_days)
        )
    )
    return list(reversed(recent_prices))
