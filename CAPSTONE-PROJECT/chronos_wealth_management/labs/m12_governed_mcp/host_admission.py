"""Host-side MCP tool admission for the M12 starter."""


TOOL_NAME = "advisor_client_portfolio"


def admitted_tools(discovered: set[str]) -> list[str]:
    """Return only capabilities this host may expose to an upstream model."""
    return sorted(tool_name for tool_name in discovered if admission_denial(tool_name) is None)


def admission_denial(tool_name: str) -> dict[str, str] | None:
    """Deny an unadmitted tool before an MCP call can be dispatched."""
    # TODO 0: return None for TOOL_NAME and a tool_not_admitted denial for all
    # other tools. This function runs before session.call_tool().
    return {"status": "not_implemented", "reason": "host_admission_not_implemented"}
