"""Compatibility exports for the advisor route owner."""

from chronos.api_routes_advisor import (
    ask_advisor_assistant,
    create_advisor_client_report,
    decide_note_draft_route,
    read_advisor_client_portfolio,
    read_advisor_clients,
    read_advisor_report,
    read_client_advisor_messages,
    read_pending_note_drafts,
    router,
)

__all__ = [
    "ask_advisor_assistant",
    "create_advisor_client_report",
    "decide_note_draft_route",
    "read_advisor_client_portfolio",
    "read_advisor_clients",
    "read_advisor_report",
    "read_client_advisor_messages",
    "read_pending_note_drafts",
    "router",
]
