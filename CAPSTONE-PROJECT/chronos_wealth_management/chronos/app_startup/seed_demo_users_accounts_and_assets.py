"""Demo users, accounts, and assets created on first run."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.shared_database.database_tables import (
    Account,
    AdvisorReport,
    Asset,
    Holding,
    Trade,
    User,
)

STARTING_CASH = 100_000.0
STARTING_SIMULATED_DATE = date(2020, 6, 1)

DEMO_USERS = [
    {"email": "alice@example.com", "name": "Alice Investor", "role": "INVESTOR"},
    {"email": "bob@example.com", "name": "Bob Investor", "role": "INVESTOR"},
    {"email": "advisor@example.com", "name": "Demo Advisor", "role": "ADVISOR"},
]

DEMO_ASSETS = [
    {"symbol": "AAPL", "name": "Apple Inc.", "asset_class": "Equity", "sector": "Technology", "risk_level": "HIGH"},
    {"symbol": "MSFT", "name": "Microsoft", "asset_class": "Equity", "sector": "Technology", "risk_level": "MEDIUM"},
    {"symbol": "SPY", "name": "S&P 500 ETF", "asset_class": "ETF", "sector": "Broad Market", "risk_level": "MEDIUM"},
    {"symbol": "GLD", "name": "Gold ETF", "asset_class": "ETF", "sector": "Metals", "risk_level": "MEDIUM"},
    {"symbol": "JPM", "name": "JPMorgan Chase", "asset_class": "Equity", "sector": "Financials", "risk_level": "MEDIUM"},
]


def seed_demo_users_accounts_and_assets(db: Session) -> None:
    for user_fields in DEMO_USERS:
        existing_user = db.scalar(select(User).where(User.email == user_fields["email"]))
        if existing_user is None:
            existing_user = User(**user_fields)
            db.add(existing_user)
            db.flush()
        if existing_user.role == "INVESTOR":
            existing_account = db.scalar(
                select(Account).where(Account.user_id == existing_user.id)
            )
            if existing_account is None:
                db.add(
                    Account(
                        user_id=existing_user.id,
                        name=f"{existing_user.name} Account",
                        cash_balance=STARTING_CASH,
                        initial_cash=STARTING_CASH,
                        simulated_date=STARTING_SIMULATED_DATE,
                    )
                )

    for asset_fields in DEMO_ASSETS:
        if db.get(Asset, asset_fields["symbol"]) is None:
            db.add(Asset(**asset_fields))

    db.flush()


def reset_demo_investor_accounts(db: Session) -> int:
    db.query(Holding).delete()
    db.query(Trade).delete()
    db.query(AdvisorReport).delete()

    accounts = db.scalars(select(Account)).all()
    for account in accounts:
        account.cash_balance = STARTING_CASH
        account.initial_cash = STARTING_CASH
        account.simulated_date = STARTING_SIMULATED_DATE

    db.flush()
    return len(accounts)
