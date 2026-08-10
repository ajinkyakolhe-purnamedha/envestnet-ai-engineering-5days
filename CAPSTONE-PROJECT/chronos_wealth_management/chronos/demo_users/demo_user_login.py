"""Demo login by email — no passwords in Module 0."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.shared_database.database_tables import User
from chronos.shared_database.domain_errors import RecordNotFoundError


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
