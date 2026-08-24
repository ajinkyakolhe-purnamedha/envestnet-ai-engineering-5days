"""Compatibility exports for the system route owner."""

from chronos.api_routes_system import (
    login_demo_user,
    read_demo_users,
    read_health,
    reset_demo_data,
    router,
)

__all__ = [
    "login_demo_user",
    "read_demo_users",
    "read_health",
    "reset_demo_data",
    "router",
]
