# Lab 12 · Govern an MCP Read Boundary

Use the participant instructions in
[`SLIDES-markdown/m12-lab-instructions.md`](../../../SLIDES-markdown/m12-lab-instructions.md).

Run from `CODEALONGS/`:

```bash
uv run python m12_governed_mcp/lab/client.py
uv run python m12_governed_mcp/lab/progress_check.py
```

`client.py` launches `starter_server.py` as a local `stdio` MCP process. The
starter is intentionally incomplete, so the progress meter initially fails.
Complete TODO 0 in `client.py` for host-side tool admission, then the three
server-policy gaps in `starter_server.py`; do not add a network call, a
secret, or a client-delivery/portfolio-mutation feature.

The lab uses synthetic Chronos facts and a classroom caller-identity fixture.
