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

The starter intentionally reports `not_ready` until learners complete its
three small server-side policy gaps. The client/server exchange itself is real
local `stdio` MCP; no network or secrets are required.

Chronos uses synthetic data and virtual money only. The final snippet creates a
pending approval request; it does not deliver a note or mutate a portfolio.
