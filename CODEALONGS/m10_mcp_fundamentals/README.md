# M10 · MCP Fundamentals Code-Along

Run these cards from `CODEALONGS/` in order:

```bash
uv run --extra courseware python m10_mcp_fundamentals/simple_mcp_client.py
uv run --extra courseware python m10_mcp_fundamentals/01_tools_are_trapped.py
uv run --extra courseware python m10_mcp_fundamentals/03_discover_and_call.py
uv run --extra courseware python m10_mcp_fundamentals/05_real_reuse_with_models.py
```

| Card | Teaches |
| --- | --- |
| `simple_mcp_server.py` + `simple_mcp_client.py` | The smallest working server/client: call a tool and read a resource |
| `01_tools_are_trapped.py` | Why direct imports couple another application to implementation details |
| `02_chronos_mcp_server.py` | How `@mcp.tool()` publishes a read-only Python capability |
| `03_discover_and_call.py` | Server process, client initialization, tool discovery, and a call |
| `05_real_reuse_with_models.py` | Two separate MCP clients give the same live facts to real local-model calls with different output boundaries |

`02_chronos_mcp_server.py` is launched automatically by Cards 03 and 05.
`04_reuse_across_agents.py` is optional reading: it shows the reuse idea in
plain text, while Card 05 proves it with two real model calls.

The server runs over local stdio and contains no governance controls. M11 and
M12 add data scope, identity, limits, and audit logging.
