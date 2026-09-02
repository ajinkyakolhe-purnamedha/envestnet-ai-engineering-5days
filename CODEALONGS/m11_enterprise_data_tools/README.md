# M11 · Connecting to Enterprise Data and Tools

M10 taught the MCP connection: publish, discover, call, and reuse. M11 asks a
different question: **what narrow business capabilities should the server
publish?** The answer is a curated data product—not raw SQL, a database
connection, or an unrestricted vendor API.

Run the three cards from this directory in order:

```bash
cd CODEALONGS/m11_enterprise_data_tools
uv run --extra courseware python 01_curated_data_product.py
uv run --extra courseware python 03_explain_live_governed_facts.py --audience investor
uv run --extra courseware python 03_explain_live_governed_facts.py --audience advisor
```

| Card | Teaches |
| --- | --- |
| `01_curated_data_product.py` | Capstone-aligned portfolio snapshot and deterministic advisor review facts |
| `02_chronos_data_server.py` | Publishing investor and advisor business contracts through MCP |
| `03_explain_live_governed_facts.py` | Real investor explanation and advisor pending-draft flows over live MCP results |

This is a classroom simulation of a trusted host calling curated read models.
It deliberately does **not** authenticate callers or authorise access to a
particular client. Module 12 wraps these same contracts with identity,
server-side authorisation, allowlists, resource controls, and audit logging.
