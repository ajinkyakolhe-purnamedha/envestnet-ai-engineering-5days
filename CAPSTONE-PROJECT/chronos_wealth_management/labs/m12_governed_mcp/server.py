"""M12 starter: govern one real Chronos read before MCP dispatch.

Students implement the three functions marked TODO. The supplied reader is
intentionally real: it calls the deterministic Chronos portfolio service only
after the policy functions permit it.
"""

import os
from typing import Any

from chronos.application_database import SessionLocal
from chronos.application_errors_and_permissions import require_advisor_user, require_investor_user
from chronos.demo_users_and_startup_data import login_demo_user_by_email
from chronos.investor_accounts_portfolios_and_history import (
    build_current_portfolio_snapshot,
    get_account_for_investor_user,
)
from labs.m12_governed_mcp.host_admission import TOOL_NAME


ASSIGNED_CLIENT_EMAILS = {"advisor_01": {"alice@example.com"}}
CALLER_ADVISOR_EMAILS = {"advisor_01": "advisor@example.com"}
UNADMITTED_TOOL_NAME = "export_all_holdings"


class M12ImplementationRequired(NotImplementedError):
    """Raised until a learner supplies one required server-side control."""


def read_bounded_portfolio(client_email: str, max_positions: int) -> dict[str, Any]:
    """Read real, simulated-date-safe Chronos facts after policy permits it."""
    with SessionLocal() as db:
        investor = require_investor_user(login_demo_user_by_email(db, client_email))
        account = get_account_for_investor_user(db, investor.id)
        portfolio = build_current_portfolio_snapshot(db, account)
        return {
            "status": "ok",
            "client_email": investor.email,
            "simulated_date": portfolio.simulated_date.isoformat(),
            "holdings": [
                {"symbol": holding.symbol, "shares": holding.shares}
                for holding in portfolio.holdings[:max_positions]
            ],
            "source": "chronos_portfolio_snapshot",
        }


def authorize_assigned_client(caller: str, client_email: str) -> dict[str, Any] | None:
    """TODO 1: deny an unassigned client before any portfolio read.

    Return ``None`` when permitted. Otherwise return a complete denial result
    with ``status``, ``reason``, and ``audit`` keys.
    """
    raise M12ImplementationRequired(
        "M12 TODO 1: authorize the trusted caller before reading a portfolio."
    )


def validate_max_positions(caller: str, max_positions: int) -> dict[str, Any] | None:
    """TODO 2: deny values outside the server's small result bound."""
    raise M12ImplementationRequired(
        "M12 TODO 2: validate max_positions before reading a portfolio."
    )


def record_audit_event(caller: str, decision: str, executed: bool) -> dict[str, Any]:
    """TODO 3: return sanitized, attributable audit evidence for every path."""
    raise M12ImplementationRequired(
        "M12 TODO 3: record a sanitized audit event for every policy decision."
    )


def _require_trusted_advisor(caller: str) -> None:
    advisor_email = CALLER_ADVISOR_EMAILS.get(caller)
    if advisor_email is None:
        raise M12ImplementationRequired(
            "M12 TODO 1: map a trusted caller to an authorized Chronos advisor."
        )
    with SessionLocal() as db:
        require_advisor_user(login_demo_user_by_email(db, advisor_email))


def handle_advisor_client_portfolio(
    caller: str, client_email: str, max_positions: int
) -> dict[str, Any]:
    """Apply student-built controls, then read one bounded client portfolio."""
    denial = authorize_assigned_client(caller, client_email)
    if denial is not None:
        return denial

    denial = validate_max_positions(caller, max_positions)
    if denial is not None:
        return denial

    _require_trusted_advisor(caller)
    result = read_bounded_portfolio(client_email, max_positions)
    result["audit"] = record_audit_event(caller, "allow", True)
    return result


def create_server():
    """Create the MCP server only when the optional M12 dependency is present."""
    from mcp.server import MCPServer

    mcp = MCPServer("Chronos M12 Governed MCP")

    @mcp.tool(name=UNADMITTED_TOOL_NAME)
    def export_all_holdings() -> dict[str, str]:
        """Deliberately unadmitted teaching tool; the host must not dispatch it."""
        return {"status": "should_not_be_called"}

    @mcp.tool()
    def advisor_client_portfolio(
        client_email: str, max_positions: int = 2
    ) -> dict[str, Any]:
        """Return a bounded portfolio for a caller-authorized client only."""
        caller = os.environ.get("M12_CALLER", "unknown")
        try:
            return handle_advisor_client_portfolio(caller, client_email, max_positions)
        except M12ImplementationRequired as error:
            # The starter must be usable before its controls are written. Make
            # that state explicit over MCP instead of inventing a portfolio or
            # allowing an ungoverned read.
            return {
                "status": "not_implemented",
                "reason": "m12_policy_controls_not_implemented",
                "error": str(error),
            }

    return mcp


def run_server() -> None:
    create_server().run(transport="stdio")


if __name__ == "__main__":
    run_server()
