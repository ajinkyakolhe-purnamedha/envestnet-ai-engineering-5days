# M10 · MCP Fundamentals Code-Along

Run these cards from `CODEALONGS/` in order:

```bash
uv run --extra courseware python m10_mcp_fundamentals/01_tools_are_trapped.py
uv run --extra courseware python m10_mcp_fundamentals/03_discover_and_call.py
uv run --extra courseware python m10_mcp_fundamentals/04_reuse_across_agents.py
```

| Card | Teaches |
| --- | --- |
| `01_tools_are_trapped.py` | Why direct imports couple a capability to one application |
| `02_chronos_mcp_server.py` | How `@mcp.tool()` publishes a read-only Python capability |
| `03_discover_and_call.py` | Server process, client initialization, tool discovery, and a call |
| `04_reuse_across_agents.py` | Investor and advisor applications reuse the same MCP tools |

The server runs over local stdio and contains no governance controls. M11 and
M12 add data scope, identity, limits, and audit logging.
