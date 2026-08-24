"""Reset demo investor accounts to their starting state.

Run from the project root:

    uv run python -m scripts.reset_demo_data
"""

from chronos.demo_users_and_startup_data import (
    reset_demo_investor_accounts,
    seed_demo_users_accounts_and_assets,
)
from chronos.application_database import (
    SessionLocal,
    create_database_tables,
)


def main() -> None:
    create_database_tables()
    session = SessionLocal()
    try:
        seed_demo_users_accounts_and_assets(session)
        accounts_reset = reset_demo_investor_accounts(session)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    print(f"Reset {accounts_reset} demo accounts.")


if __name__ == "__main__":
    main()
