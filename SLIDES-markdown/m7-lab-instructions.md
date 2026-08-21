> **⚠️ OUTDATED** — These lab instructions are out of date (paths and setup
> may no longer match the repo). Reworked labs are coming later.

# M7 Lab Instructions

## Goal

Build a simple ReAct-style advisor research assistant in pure Python.

The assistant should answer:

```text
Can Alice add more AAPL under the guidelines? Show the facts you checked.
```

Core rule:

```text
The model requests. Python executes.
```

The required lab path uses deterministic planning first. Local SmolLM2 planning
is optional after the loop works.

## Part 1: Notebook Lab

Open this notebook:

```text
CODEALONGS/code_alongs/07b_m7_manual_agent_loop.ipynb
```

Run from the `CODEALONGS/` folder:

```bash
uv sync --extra courseware
uv run jupyter lab
```

Run the notebook from top to bottom.

## Required Tools

Implement these tools:

```text
get_current_price(symbol)
get_portfolio_allocation(client_id)
check_guidelines(symbol, proposed_allocation_pct)
```

Each tool must have a Pydantic argument schema.

## Required Runtime Pieces

The agent loop should include:

- `messages`: transcript plus tool observations;
- planner: returns either a tool request or a final answer;
- JSON tool request shape: `{"tool": "...", "args": {...}}`;
- Pydantic validation before execution;
- tool registry: maps tool names to Python functions;
- bounded loop: `max_turns = 5`;
- telemetry trace for every tool attempt.

## Success Criteria

Done when the notebook prints:

- final advisor answer;
- price fact checked;
- portfolio allocation fact checked;
- guideline fact checked;
- trace records for tool calls;
- useful error output for at least one malformed tool request.

## Part 2: Optional Capstone Integration

The notebook version uses synthetic in-memory data. The Capstone version should
connect the same loop to Chronos Wealth backend data.

Capstone project root:

```text
CAPSTONE-PROJECT/chronos_wealth_management
```

Recommended backend location for the agent:

```text
chronos/advisor_workspace/run_advisor_research_agent.py
```

Put these pieces in that new file:

- Pydantic tool argument schemas;
- Chronos-backed tool functions;
- `TOOL_SCHEMAS`;
- `TOOL_FUNCTIONS`;
- `execute_with_trace`;
- deterministic planner;
- `run_advisor_research_agent(db, advisor_user_id, client_user_id, question)`.

## Capstone Tool Hints

### `get_current_price(symbol)`

Use the client's simulated date and existing market price query.

Relevant existing code:

```text
chronos/market_price_queries/find_price_for_simulated_date.py
chronos/investor_accounts/get_investor_account.py
```

The tool should:

1. load the client account;
2. read `account.simulated_date`;
3. call the existing price lookup for the requested symbol;
4. return a small dictionary with symbol, date, and price.

### `get_portfolio_allocation(client_id)`

Use the existing portfolio snapshot builder.

Relevant existing code:

```text
chronos/portfolio_performance/calculate_current_portfolio_value.py
chronos/advisor_workspace/generate_advisor_review_report.py
```

The tool should:

1. load the client's investor account;
2. call `build_current_portfolio_snapshot`;
3. return total value, cash percentage, and holding allocation percentages.

### `check_guidelines(symbol, proposed_allocation_pct)`

Keep this deterministic.

Suggested first rule:

```text
No single holding should exceed 35% allocation.
```

The tool should return:

```python
{
    "symbol": symbol,
    "proposed_allocation_pct": proposed_allocation_pct,
    "allowed": proposed_allocation_pct <= 35.0,
    "limit_pct": 35.0,
}
```

## Capstone API Hints

Add response schemas in:

```text
chronos/shared_database/api_schemas.py
```

Suggested schemas:

```python
class AdvisorResearchTraceRecord(BaseModel):
    turn: int
    tool: str | None = None
    args: dict = {}
    result: dict | None = None
    exception: str | None = None
    elapsed_ms: float

class AdvisorResearchAgentResponse(BaseModel):
    advisor_user_id: int
    client_user_id: int
    question: str
    final_answer: str
    facts_checked: list[str]
    trace: list[AdvisorResearchTraceRecord]
```

Expose a route in:

```text
chronos/api_routes/advisor_workspace_routes.py
```

Suggested route:

```python
@router.post(
    "/advisor/clients/{client_user_id}/research-agent",
    response_model=AdvisorResearchAgentResponse,
)
def run_advisor_research_agent_route(
    client_user_id: int,
    advisor_user_id: int,
    question: str,
    db: Session = Depends(get_database_session),
):
    with translate_domain_errors():
        return run_advisor_research_agent(
            db=db,
            advisor_user_id=advisor_user_id,
            client_user_id=client_user_id,
            question=question,
        )
```

## Capstone UI Hints

Add API client function in:

```text
ui/api_client.py
```

Suggested function:

```python
def run_advisor_research_agent(
    advisor_user_id: int, client_user_id: int, question: str
) -> dict:
    return _raise_for_status(
        requests.post(
            f"{API_BASE_URL}/advisor/clients/{client_user_id}/research-agent",
            params={"advisor_user_id": advisor_user_id, "question": question},
        )
    ).json()
```

Add a small Advisor Dashboard section in:

```text
ui/advisor_dashboard_screen.py
```

Suggested UI:

- text input for advisor question;
- button: `Run Research Assistant`;
- final answer display;
- trace table display.

## Testing Hints

Add backend tests in:

```text
tests/test_advisor_research_agent.py
```

Minimum tests:

1. advisor can run research agent for Alice;
2. investor cannot run advisor research agent;
3. response includes final answer;
4. trace includes all three tools;
5. malformed tool arguments become trace exceptions.

Run from:

```text
CAPSTONE-PROJECT/chronos_wealth_management
```

```bash
uv run pytest
```

## Stretch Options

Only after the deterministic loop works:

- replace deterministic planner with local SmolLM2 planner;
- save trace records as JSONL;
- persist research assistant runs in a database table;
- add a stricter guideline policy;
- let the advisor choose the proposed allocation percentage.
