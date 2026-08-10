"""Server-side role checks for investor and advisor features."""

from chronos.shared_database.database_tables import User
from chronos.shared_database.domain_errors import WrongRoleError

INVESTOR_ROLE = "INVESTOR"
ADVISOR_ROLE = "ADVISOR"


def require_investor_user(user: User) -> User:
    if user.role != INVESTOR_ROLE:
        raise WrongRoleError(f"User {user.id} is {user.role}, not an investor")
    return user


def require_advisor_user(user: User) -> User:
    if user.role != ADVISOR_ROLE:
        raise WrongRoleError(f"User {user.id} is {user.role}, not an advisor")
    return user
