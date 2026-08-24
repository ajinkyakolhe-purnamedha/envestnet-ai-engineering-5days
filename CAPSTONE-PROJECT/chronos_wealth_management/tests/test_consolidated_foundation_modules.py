"""Import checks for the consolidated Chronos foundation modules."""

from chronos.application_database import Account, SessionLocal, User
from chronos.application_errors_and_permissions import ADVISOR_ROLE, INVESTOR_ROLE
from chronos.demo_users_and_startup_data import DEMO_USERS, STARTING_CASH


def test_foundation_modules_export_expected_names():
    assert User.__name__ == "User"
    assert Account.__name__ == "Account"
    assert SessionLocal is not None
    assert INVESTOR_ROLE == "INVESTOR"
    assert ADVISOR_ROLE == "ADVISOR"
    assert STARTING_CASH == 100_000.0
    assert [user["email"] for user in DEMO_USERS] == [
        "alice@example.com",
        "bob@example.com",
        "advisor@example.com",
    ]
