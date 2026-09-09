"""Application-level containment for a model-proposed data request."""

from __future__ import annotations

from uuid import uuid4

from pydantic import BaseModel, Field, ValidationError


class PortfolioRequest(BaseModel):
    tool: str
    client_id: str
    max_positions: int = Field(ge=1, le=2)


admitted_tools = {"get_portfolio_summary"}
assigned_clients = {"advisor_01": {"alice"}}


def evaluate_request(request: dict[str, object], caller_id: str, step_count: int = 1) -> dict[str, object]:
    """Admit, scope, bound, then read a tiny synthetic result—or deny first."""

    audit = {"request_id": uuid4().hex, "caller": caller_id, "tool": request.get("tool")}
    if step_count > 2:
        return {"status": "contained", "reason": "step_limit_reached", "audit": audit, "result": None}
    try:
        parsed_request = PortfolioRequest.model_validate(request)
    except ValidationError:
        return {"status": "blocked", "reason": "request_contract_invalid", "audit": audit, "result": None}
    if parsed_request.tool not in admitted_tools:
        return {"status": "blocked", "reason": "tool_not_admitted", "audit": audit, "result": None}
    if parsed_request.client_id not in assigned_clients.get(caller_id, set()):
        return {"status": "blocked", "reason": "client_not_assigned", "audit": audit, "result": None}
    result = {
        "client": parsed_request.client_id,
        "positions": ["SPY", "AAPL"][: parsed_request.max_positions],
        "as_of_date": "2026-09-08",
        "source": "synthetic approved portfolio view",
    }
    return {"status": "allowed", "reason": "bounded_read", "audit": audit, "result": result}
