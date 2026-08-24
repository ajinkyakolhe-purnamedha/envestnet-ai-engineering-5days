"""Compatibility exports for the investor route owner."""

from chronos.api_routes_investor import (
    read_supported_assets,
    read_symbol_price_history,
    router,
)

__all__ = ["read_supported_assets", "read_symbol_price_history", "router"]
