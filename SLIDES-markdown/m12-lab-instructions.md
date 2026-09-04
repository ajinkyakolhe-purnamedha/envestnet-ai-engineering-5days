# Lab 12 · Govern an MCP Read Boundary

**Duration:** 60 minutes

**Goal:** Complete a small, real local MCP boundary that admits only the
approved review tool, permits a bounded review for Alice, rejects an advisor
request for unassigned Bob before any data is read, rejects an over-limit
request, and records attributable audit evidence.

Chronos data in this lab is synthetic and all money is virtual. This lab does
not authenticate a real user, call a network service, deliver a client note,
or mutate a portfolio. `M12_CALLER` is a supplied classroom fixture standing
in for trusted host identity.

## Part 1 · See the unfinished boundary run (0–8 minutes)

From `CODEALONGS/`, run:

```bash
uv run python m12_governed_mcp/lab/client.py
uv run python m12_governed_mcp/lab/progress_check.py
```

`client.py` starts `starter_server.py` as a separate local `stdio` MCP
process. Confirm that the server discovers both `advisor_client_review` and
`export_all_holdings`. The host initially admits neither, so the progress
check is expected to fail before it makes the three intended MCP calls:

| Call | Intended outcome after the lab |
| --- | --- |
| Alice, `max_positions=2` | permitted bounded facts + allow audit |
| Bob, `max_positions=2` | denied before the data service + deny audit |
| Alice, `max_positions=3` | denied by validation + deny audit |

The initial progress check is expected to fail: the starter deliberately
returns `not_ready` until you implement the deterministic policy gaps.

## Part 2 · Admit tools at the host (8–18 minutes)

Open `m12_governed_mcp/lab/client.py`. The server advertises a deliberately
excluded `export_all_holdings` tool alongside the useful review tool. Complete
**TODO 0** in `admit_tool()`.

- Return `None` only for `advisor_client_review`.
- Return `status: "denied"` and `reason: "tool_not_admitted"` for every other
  tool.
- The client must calculate `MODEL_VISIBLE` from this policy and deny the
  excluded tool before `session.call_tool()`.

Use `01_admit_tools.py` as the reference. Explain why discovery is not an
instruction to expose every server capability to a model.

## Part 3 · Add server-side authorisation (18–30 minutes)

Open `m12_governed_mcp/lab/starter_server.py`. `ASSIGNED_CLIENTS` is the
server's deterministic policy fixture. Complete **TODO 1** so that a caller
may request only an assigned client.

Rules:

- Read the caller only from `M12_CALLER`; never accept caller identity from the
  model's tool arguments.
- Reject Bob with `status: "denied"` and `reason: "unassigned_client"`.
- Return immediately. `read_client_review()` must not run for Bob.

Use `02_authorize_before_read.py` as the teaching reference. Run `client.py`
again and inspect the Bob response before moving on.

## Part 4 · Add deterministic result validation (30–39 minutes)

Complete **TODO 2**. A permitted caller may request only one or two positions.

- Reject any other value with `reason: "max_positions_must_be_1_or_2"`.
- Validate before calling `read_client_review()`.
- On the permitted path, return no more than the requested number of holdings.

Use `03_bound_result.py` as the reference. Explain to a partner why a typed
integer parameter is not enough: the application still needs a business bound.

## Part 5 · Record policy evidence (39–51 minutes)

Complete **TODO 3** and use it on every exit path.

Each returned audit object must include:

```text
correlation_id
caller
tool
decision
downstream_executed
```

For each denial, `downstream_executed` must be `False`. For Alice's permitted
read, it must be `True`. Keep audit data sanitized: do not log a full portfolio,
secrets, or tool result. `04_governed_chronos_server.py` shows the small
classroom audit pattern.

## Part 6 · Prove the four controls over MCP (51–58 minutes)

Run:

```bash
uv run python m12_governed_mcp/lab/progress_check.py
```

The checker starts the MCP client, which starts your server. It should report
six passes: discovery, host admission before dispatch, permitted bounded read,
unassigned-client denial, over-limit denial, and audit evidence. Do not claim
a policy works because a function looks correct—the live client/server
exchange is the evidence.

## Part 7 · Inspect the complete teaching example (58–60 minutes)

Compare your result with the assembled code-along only after your checker
passes:

```bash
uv run python m12_governed_mcp/08_complete_walkthrough.py
```

Discuss these boundaries:

| M12 owns | Later modules extend |
| --- | --- |
| host tool admission, caller scope, validation, bounded MCP results, audit | M13 full-app tests/evals; M14 hardening and attack scenarios; M15 production tracing, deployment, ownership |

**Exit criteria:** show the host's excluded-tool denial and the three MCP
responses. Explain, from control flow and audit evidence, why neither the
excluded tool nor Bob's request reached the data service.

## Capstone extension · Govern real Chronos facts

The classroom server above is deliberately standalone. To apply the same M12
controls to the completed Chronos capstone, work from
`CAPSTONE-PROJECT/chronos_wealth_management`:

```bash
uv sync --extra m12
uv run --extra m12 python -m labs.m12_governed_mcp.client
uv run --extra m12 python -m labs.m12_governed_mcp.progress_check
```

The capstone starter in `labs/m12_governed_mcp/server.py` launches a real
local `stdio` MCP server and reads the existing, simulated-date-safe Chronos
portfolio only after the controls pass. It starts visibly incomplete: each
MCP call returns `status: "not_implemented"`; it never substitutes sample
portfolio facts.

Complete the same four responsibilities in the capstone starter:

0. admit only `advisor_client_portfolio` at the host and deny
   `export_all_holdings` before dispatch;
1. authorize the trusted caller for `alice@example.com` and deny the provided
   unassigned-client case before a database read;
2. accept only one or two positions before the portfolio reader runs; and
3. attach a sanitized audit event to every allowed or denied outcome.

The capstone uses no LLM in M12. Its Streamlit M12 lab page links learners to
this local starter; the MCP client and progress check provide the live
client/server proof.
