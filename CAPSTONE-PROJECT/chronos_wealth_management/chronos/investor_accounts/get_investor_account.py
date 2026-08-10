"""Investor account lookup and response mapping."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.shared_database.api_schemas import AccountResponse
from chronos.shared_database.database_tables import Account
from chronos.shared_database.domain_errors import RecordNotFoundError


def get_account_for_investor_user(db: Session, user_id: int) -> Account:
    account = db.scalar(select(Account).where(Account.user_id == user_id))
    if account is None:
        raise RecordNotFoundError(f"No account for user {user_id}")
    return account


def build_investor_account_response(account: Account) -> AccountResponse:
    return AccountResponse(
        account_id=account.id,
        user_id=account.user_id,
        name=account.name,
        cash_balance=account.cash_balance,
        initial_cash=account.initial_cash,
        simulated_date=account.simulated_date,
    )
