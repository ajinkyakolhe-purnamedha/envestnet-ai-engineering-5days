# Lab 11 · Add MCP Agents to Chronos Wealth

**Duration:** 60 minutes

**Goal:** Apply the M11 miniature pattern to the existing Chronos Wealth
capstone. Build narrow, read-only MCP capabilities over its real deterministic
services, then use their live results in two small agent flows:

- Alice Investor receives an educational explanation of her own portfolio.
- Demo Advisor receives an internal client-review draft; it remains subject to
  Chronos’s existing approval workflow.

Do not rebuild the database, FastAPI routes, Streamlit dashboards, portfolio
calculation, or login screens. They are already the product under study.

## Part 1 · Map the product before editing it (0–10 minutes)

Open `CAPSTONE-PROJECT/chronos_wealth_management/` and identify these existing
production seams:

| Product responsibility | Existing Chronos service | File |
| --- | --- | --- |
| Current investor facts | `build_current_portfolio_snapshot()` | `chronos/investor_accounts_portfolios_and_history.py` |
| Deterministic review metrics | `analyze_client_portfolio()` | `chronos/advisor_analysis_reports_and_client_lists.py` |
| Advisor report | `generate_advisor_review_report()` | `chronos/advisor_analysis_reports_and_client_lists.py` |
| Advisor draft / approval | `submit_advisor_note_for_approval()` | `chronos/advisor_assistant_runtime.py` |
| Role checks | `require_investor_user()` / `require_advisor_user()` | `chronos/application_errors_and_permissions.py` |

Explain to a partner why the lab should call these functions rather than query
the SQLite tables directly.

## Part 2 · Define two MCP data-product contracts (10–20 minutes)

In the capstone project, create `chronos/m11_mcp_server.py`. Add the MCP
dependency for this lab environment:

```bash
cd CAPSTONE-PROJECT/chronos_wealth_management
uv add mcp
```

Design these two **read-only** contracts before writing their bodies:

| Tool | Inputs | Result must include |
| --- | --- | --- |
| `investor_portfolio_view` | `investor_user_id`, `max_positions` | bounded portfolio, simulated date, source |
| `advisor_client_review` | `advisor_user_id`, `client_user_id` | deterministic metrics, recommendations, simulated date, source |

Do not expose `run_sql`, a generic API proxy, a trade capability, or a write
tool. `max_positions` must have a small upper bound.

## Part 3 · Wrap real deterministic services (20–35 minutes)

Use the application’s database session and existing role/service functions in
your MCP server. The structure should resemble:

```python
@mcp.tool()
def investor_portfolio_view(investor_user_id: int, max_positions: int = 3) -> dict:
    with SessionLocal() as db:
        investor = require_investor_user(get_demo_user_by_id(db, investor_user_id))
        account = get_account_for_investor_user(db, investor.id)
        snapshot = build_current_portfolio_snapshot(db, account)
        # Return only the requested number of holdings plus simulated-date provenance.
```

For `advisor_client_review`, use `require_advisor_user`, then obtain the
client’s snapshot and call `analyze_client_portfolio`. Return the metrics and
recommendations, not a raw database object.

At the end of this step, confirm both tool responses include:

```text
source: chronos deterministic service layer
as_of:  the client account’s simulated date
```

## Part 4 · Build two tiny agent flows (35–50 minutes)

Create `chronos/m11_agent_flows.py` or an equivalent small runner. It starts
your local MCP server, calls the approved tool, then supplies only the tool
result to the local-model prompt.

```text
Investor flow
  investor_portfolio_view(Alice)
  → model: educational explanation only; no trade recommendation

Advisor flow
  advisor_client_review(Demo Advisor, Alice)
  → model: internal client-review draft only
  → existing Chronos approval queue before client visibility
```

Use the local model path already established earlier in the course. Do not
replace a failed model call with a canned answer: surface the environment error
and fix it.

## Part 5 · Demonstrate the two experiences (50–57 minutes)

Run both flows and capture:

1. Alice’s bounded portfolio facts and educational output.
2. Demo Advisor’s metrics/recommendations and internal draft.
3. The simulated date and source returned by each MCP tool.

The investor flow must not call the advisor review tool. The advisor flow must
not trade or publish directly to Alice; it must hand off to the existing
approval path.

## Part 6 · Review the M11/M12 boundary (57–60 minutes)

The existing demo login and role checks are useful application context. They
are not yet a complete MCP-security design. In M12, add/enforce:

- authenticated caller identity at the MCP boundary;
- server-side authorization for investor/client scope;
- tool allowlists and resource limits;
- structured audit events and a proven safe-overreach failure.

**Exit criteria:** the team can point from a miniature M11 snippet to its
production Chronos equivalent, show both real agent flows, and explain why the
MCP server exposes business contracts instead of database access.
