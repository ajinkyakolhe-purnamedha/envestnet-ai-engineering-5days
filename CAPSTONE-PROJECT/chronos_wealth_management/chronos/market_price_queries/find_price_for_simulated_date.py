"""Point-in-time price lookup: latest price on or before a simulated date."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.shared_database.database_tables import Asset, Price
from chronos.shared_database.domain_errors import (
    PriceUnavailableError,
    RecordNotFoundError,
)


def get_latest_price_on_or_before_date(
    db: Session, symbol: str, simulated_date: date
) -> Price:
    price = db.scalar(
        select(Price)
        .where(Price.symbol == symbol, Price.date <= simulated_date)
        .order_by(Price.date.desc())
        .limit(1)
    )
    if price is None:
        raise PriceUnavailableError(
            f"No price for {symbol} on or before {simulated_date}"
        )
    return price


def get_supported_assets(db: Session) -> list[Asset]:
    return list(db.scalars(select(Asset).order_by(Asset.symbol)))


def require_supported_asset(db: Session, symbol: str) -> Asset:
    asset = db.get(Asset, symbol.upper())
    if asset is None:
        raise RecordNotFoundError(f"Unknown symbol {symbol!r}")
    return asset
