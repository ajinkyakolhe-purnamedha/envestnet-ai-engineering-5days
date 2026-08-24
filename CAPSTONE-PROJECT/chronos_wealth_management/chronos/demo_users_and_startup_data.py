"""Demo users, startup data, login queries, and reset behavior."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.application_database import Account, AdvisorReport, Asset, Holding, Trade, User
from chronos.application_errors_and_permissions import RecordNotFoundError

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


def list_demo_users(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.id)))


def login_demo_user_by_email(db: Session, email: str) -> User:
    normalized_email = email.strip().lower()
    user = db.scalar(select(User).where(User.email == normalized_email))
    if user is None:
        raise RecordNotFoundError(f"No demo user with email {normalized_email!r}")
    return user


def get_demo_user_by_id(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise RecordNotFoundError(f"No user with id {user_id}")
    return user


def seed_demo_users_accounts_and_assets(db: Session) -> None:
    for user_fields in DEMO_USERS:
        user = db.scalar(select(User).where(User.email == user_fields["email"]))
        if user is None:
            user = User(**user_fields)
            db.add(user)
            db.flush()
        if user.role == "INVESTOR" and db.scalar(select(Account).where(Account.user_id == user.id)) is None:
            db.add(Account(user_id=user.id, name=f"{user.name} Account", cash_balance=STARTING_CASH, initial_cash=STARTING_CASH, simulated_date=STARTING_SIMULATED_DATE))
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
