"""Compatibility exports for the investor route owner."""

from chronos.api_routes_investor import (
    execute_trade,
    preview_trade,
    read_investor_trades,
    router,
)

__all__ = ["execute_trade", "preview_trade", "read_investor_trades", "router"]
