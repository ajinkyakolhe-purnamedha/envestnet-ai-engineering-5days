"""Trade history for an investor account."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.shared_database.database_tables import Trade


def list_trades_for_investor_account(db: Session, account_id: int) -> list[Trade]:
    return list(
        db.scalars(
            select(Trade).where(Trade.account_id == account_id).order_by(Trade.id)
        )
    )
