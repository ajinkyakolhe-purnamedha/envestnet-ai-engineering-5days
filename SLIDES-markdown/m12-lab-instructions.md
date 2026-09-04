# Lab 12 · Govern an MCP Read Boundary

**Duration:** 60 minutes

**Goal:** Complete a small, real local MCP server that permits a bounded review
for Alice, rejects an advisor request for unassigned Bob before any data is
read, rejects an over-limit request, and records attributable audit evidence.

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
process. Confirm that it discovers `advisor_client_review` and makes three
real MCP calls:

| Call | Intended outcome after the lab |
| --- | --- |
| Alice, `max_positions=2` | permitted bounded facts + allow audit |
| Bob, `max_positions=2` | denied before the data service + deny audit |
| Alice, `max_positions=3` | denied by validation + deny audit |

The initial progress check is expected to fail: the starter deliberately
returns `not_ready` until you implement the deterministic policy gaps.

## Part 2 · Add server-side authorisation (8–22 minutes)

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

## Part 3 · Add deterministic result validation (22–32 minutes)

Complete **TODO 2**. A permitted caller may request only one or two positions.

- Reject any other value with `reason: "max_positions_must_be_1_or_2"`.
- Validate before calling `read_client_review()`.
- On the permitted path, return no more than the requested number of holdings.

Use `03_bound_result.py` as the reference. Explain to a partner why a typed
integer parameter is not enough: the application still needs a business bound.

## Part 4 · Record policy evidence (32–45 minutes)

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

## Part 5 · Prove the three outcomes over MCP (45–55 minutes)

Run:

```bash
uv run python m12_governed_mcp/lab/progress_check.py
```

The checker starts the MCP client, which starts your server. It should report
five passes: discovery, permitted bounded read, unassigned-client denial,
over-limit denial, and audit evidence. Do not claim a policy works because a
function looks correct—the live client/server exchange is the evidence.

## Part 6 · Inspect the complete teaching example (55–60 minutes)

Compare your result with the assembled code-along only after your checker
passes:

```bash
uv run python m12_governed_mcp/08_complete_walkthrough.py
```

Discuss these boundaries:

| M12 owns | Later modules extend |
| --- | --- |
| host tool admission, caller scope, validation, bounded MCP results, audit | M13 full-app tests/evals; M14 hardening and attack scenarios; M15 production tracing, deployment, ownership |

**Exit criteria:** show the three MCP responses and explain, from control flow
and audit evidence, why Bob's data service was never reached.
