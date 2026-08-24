"""Compatibility exports for the investor route owner."""

from chronos.api_routes_investor import (
    read_account_value_history,
    read_investor_account,
    read_investor_portfolio,
    router,
)

__all__ = [
    "read_account_value_history",
    "read_investor_account",
    "read_investor_portfolio",
    "router",
]
