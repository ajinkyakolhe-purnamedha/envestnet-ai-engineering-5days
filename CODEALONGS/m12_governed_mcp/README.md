# M12 · Governed MCP Integration

Each small snippet teaches one policy decision without requiring slides.

Run from `CODEALONGS/`:

```bash
uv run python m12_governed_mcp/00_governed_request.py
uv run python m12_governed_mcp/01_admit_tools.py
uv run python m12_governed_mcp/02_authorize_before_read.py
uv run python m12_governed_mcp/03_bound_result.py
uv run python m12_governed_mcp/05_permit_deny_prove.py
uv run python m12_governed_mcp/06_approval_required.py
uv run python m12_governed_mcp/08_complete_walkthrough.py
```

Start with `00_governed_request.py`: it maps one allowed and one denied
request in ordinary Python. The following snippets zoom in on each decision.

`05_permit_deny_prove.py` starts `04_governed_chronos_server.py` as a real
local `stdio` MCP process. It prints tool discovery, an allowed Alice read,
and a denied Bob request. `M12_CALLER` is a classroom identity fixture, not a
production authentication design.

`08_complete_walkthrough.py` starts `07_complete_governed_server.py`. Read
that final server after the short snippets: it combines the approved MCP
surface, caller scope, validation, bounded facts, audit events, and an
approval-required draft in one runnable service.

## 60-minute lab

The lab starter is in [`lab/README.md`](lab/README.md). From `CODEALONGS/`,
run its real local MCP client and progress meter:

```bash
uv run python m12_governed_mcp/lab/client.py
uv run python m12_governed_mcp/lab/progress_check.py
```

The starter intentionally reports `not_ready` until learners complete four
small controls: host-side admission of `advisor_client_review`, followed by
server-side client-scope authorisation, `max_positions` validation, and audit
evidence. The server also advertises `export_all_holdings` so learners can
prove that discovery does not make a tool model-visible or callable. The
client/server exchange itself is real local `stdio` MCP; no network or secrets
are required.

## Capstone extension

After the standalone lab, apply the same controls to real synthetic Chronos
portfolio facts from `CAPSTONE-PROJECT/chronos_wealth_management`:

```bash
uv sync --extra m12
uv run --extra m12 python -m labs.m12_governed_mcp.client
uv run --extra m12 python -m labs.m12_governed_mcp.progress_check
```

See `CAPSTONE-PROJECT/chronos_wealth_management/labs/m12_governed_mcp/README.md`
for the four capstone TODOs. Its MCP server reads the simulated-date-safe
portfolio only after host admission, caller scope, and bounds permit the call.

Chronos uses synthetic data and virtual money only. The final snippet creates a
pending approval request; it does not deliver a note or mutate a portfolio.
