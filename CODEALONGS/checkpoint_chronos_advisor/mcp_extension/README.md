# Module 10 · MCP Fundamentals — Chronos Tools

This is the Module 10 extension of the checkpoint lab. It moves two read-only
Chronos capabilities behind an MCP boundary:

- `portfolio_summary(client_id)`
- `search_policy(query)`

Run the complete client/server example from `CODEALONGS/`:

```bash
uv run --extra courseware python checkpoint_chronos_advisor/mcp_extension/client.py
```

The client starts the stdio server, discovers its tools, and calls both. The
next module adds curated data products, server-side scope, limits, and audit
logging.

## Same server, two AI applications

```bash
uv run --extra courseware python checkpoint_chronos_advisor/mcp_extension/investor_agent.py
uv run --extra courseware python checkpoint_chronos_advisor/mcp_extension/advisor_agent.py
```

Both scripts make live calls to the same MCP server. The investor agent turns
the results into an educational explanation; the advisor agent turns them into
an internal meeting brief. MCP reuses capabilities, not one agent's behaviour.
