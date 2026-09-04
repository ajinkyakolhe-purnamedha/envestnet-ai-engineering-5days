# M12 Chronos Governed MCP Starter

This starter wraps real Chronos portfolio facts in one approved local MCP
tool. It is incomplete by design: TODO 0 admits the tool at the host, and the
three policy functions in `server.py` then govern the read.

Run from `CAPSTONE-PROJECT/chronos_wealth_management`:

```bash
uv sync --extra m12
uv run --extra m12 python -m labs.m12_governed_mcp.client
uv run --extra m12 python -m labs.m12_governed_mcp.progress_check
```

Implement, in order:

0. `host_admission.py` — expose only `advisor_client_portfolio` from MCP
   discovery and deny `export_all_holdings` before dispatch.
1. `authorize_assigned_client()` — reject an unassigned client before opening
   a database session. Return `None` when allowed, otherwise a denial result
   with a sanitized audit event.
2. `validate_max_positions()` — permit only `1` or `2`, before any portfolio
   read. Return `None` when allowed, otherwise a denial result and audit.
3. `record_audit_event()` — create a sanitized event with `correlation_id`,
   `caller`, `tool`, `decision`, and `downstream_executed`.

The supplied `read_bounded_portfolio()` is intentionally real. It calls the
existing Chronos portfolio snapshot only after both controls permit the call;
it never reads future prices and exposes no trading capability.
