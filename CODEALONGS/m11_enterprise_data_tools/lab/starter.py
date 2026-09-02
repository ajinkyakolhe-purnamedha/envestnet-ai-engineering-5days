"""Lab 11 starter: enforce a supplied advisor scope before the read model.

This is a capability-contract exercise. M12 replaces this supplied scope with
authenticated identity and server-side authorisation.
"""

from pathlib import Path
import sys

M11_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(M11_DIR))

from governed_data_product import portfolio_view


ADVISOR_SCOPE = {"allowed_clients": {"alice"}, "max_positions": 2}


def advisor_portfolio_view(client_id: str, max_positions: int) -> dict:
    """Return a bounded view only when the supplied teaching scope permits it."""
    # TODO 1: reject client IDs outside ADVISOR_SCOPE["allowed_clients"].
    # TODO 2: reject max_positions above ADVISOR_SCOPE["max_positions"].
    # TODO 3: call portfolio_view only after both checks succeed.
    raise NotImplementedError("Complete the three lab checks.")


if __name__ == "__main__":
    print(advisor_portfolio_view("alice", 2))
