---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M12 · Governed MCP Integration

MCP makes capabilities reusable.

Governance decides whether a proposed call may happen.

<!-- Timing: 1 minute. By the end, participants should be able to make an MCP boundary reject an unsafe proposal before it reaches Chronos data or a consequential action. This is not a module about persuading a model to behave. It is about deterministic controls that still work when a model is wrong or manipulated. -->

---

# M11 made a useful capability. M12 controls its authority.

```text
M11: a small business contract returns bounded, useful facts

M12: policy decides who may call it, for which client, with which bounds
```

<!-- Timing: 3 minutes. Recall M11's advisor_client_review teaching example: it is narrow and read-only, but it is still risky if any caller can ask for any client or unbounded result. Keep the boundary clear: M12 governs the MCP connection and call. M13–M15 will test, harden, and operate the complete AI application. -->

---

<!-- _class: lead -->

# Start with one request that must be safe

```text
model proposes a tool + arguments
        ↓
bounded facts or a controlled denial
```

<!-- Timing: 1 minute. Start with the outcome rather than a list of controls. The same request shape can be permitted or denied; the next slides reveal where that decision belongs. -->

---

# One safe request, step by step

```text
model proposes a tool + arguments
        ↓
host admits a tool
        ↓
server authorises and validates
        ↓
bounded facts or controlled denial + audit event
```

<!-- Timing: 2 minutes. Advance through the arrows slowly. “Model proposes” is the important phrase: a proposal is input, not proof of authority. We will see a permitted Alice request and an unassigned-client request that must stop before a read. -->

---

# A model proposal is never the decision

Source: `m12_governed_mcp/00_governed_request.py`

```text
Model proposes: advisor_client_review('alice')
ALLOW alice: bounded Chronos facts

Model proposes: advisor_client_review('bob')
DENY bob: unassigned_client; no data read
```

<!-- Timing: 3 minutes. Run the overview snippet. Ask learners what changed between Alice and Bob: not the model's intent, but deterministic client assignment. This is ordinary Python by design; establish the policy path before protocol details return. -->

---

# Discovery does not grant model access

Source: `m12_governed_mcp/01_admit_tools.py`

```python
discovered = {"advisor_client_review", "export_all_holdings"}
approved = {"advisor_client_review"}

model_visible = sorted(discovered & approved)
```

```text
Model-visible: ['advisor_client_review']
Excluded: ['export_all_holdings']
```

<!-- Timing: 3 minutes. Run the snippet. Discovery is information from another boundary, not an instruction to expose everything. Tool descriptions, resources, and prompts can be misleading or injected, so the host owns admission. -->

---

# Permission is not identity

```text
Who connected?       identity establishes a credible caller
May they access it?  server policy establishes permission
```

`M12_CALLER` is a classroom fixture, not production authentication.

<!-- Timing: 2 minutes. Make the vocabulary distinction explicit before showing the authorization code. A prompt that claims a role is neither identity nor permission. In production, connection identity depends on the deployed transport and organisation. -->

---

# The server checks scope before it reads facts

Source: `m12_governed_mcp/02_authorize_before_read.py`

```python
if client_id not in assigned_clients[caller_id]:
    print("DENY ... read service not called")
    return

print("ALLOW ...", read_client_review(client_id))
```

<!-- Timing: 3 minutes. Run it and point to control flow: the data service is below the scope check. Server-side authorisation is enforceable even when the upstream model or host is wrong. -->

---

# Stop before data access

```text
Unassigned client request
        ↓
DENY: unassigned_client
        ↓
read service is never called
```

The denial is evidence of a control working—not a failed model response.

<!-- Timing: 3 minutes. Pause here for a prediction: where would a bug be if Bob's data appeared in a denial message? Emphasize early return and no downstream execution; that evidence matters more than a polite error message. -->

---

# A permitted read still needs deterministic limits

Source: `m12_governed_mcp/03_bound_result.py`

```python
if max_positions not in {1, 2}:
    print("DENY: max_positions must be 1 or 2")
    return

result = positions[:max_positions]
```

<!-- Timing: 3 minutes. Run the snippet. An allowed client is not an unlimited client. First show the rejection, then the bounded successful result. -->

---

# A limit is a policy decision

```text
Typed integer      → technically valid input
1 or 2 positions  → permitted business request
```

Bounds protect data exposure, model context, and predictable cost.

<!-- Timing: 2 minutes. The schema/type is only a first gate; business policy supplies the meaningful bound. Briefly name other server-enforced limits—fields, rows, duration, concurrency, and spend—without teaching a generic rate-limiting framework. -->

---

# Four questions, four deterministic controls

| Question | Control | Evidence |
| --- | --- | --- |
| Who connected? | authenticated identity | trusted caller context |
| May they access this client? | server authorisation | no read on denial |
| Is this request acceptable? | validation and limits | bounded arguments |
| What happened? | audit event | correlation + decision |

Prompts may explain policy. Python and the server enforce it.

<!-- Timing: 3 minutes. This is a vocabulary checkpoint. Ask learners to classify the earlier decisions. “Approved tool” is host admission; “assigned client” is server authorization; max_positions is validation and containment. -->

---

<!-- _class: lead -->

# Now prove the same path over real MCP

```text
client process ── stdio ──> governed server process
```

<!-- Timing: 1 minute. Re-enter the MCP runtime boundary from M10. Local stdio gives a real process and protocol exchange without network, credentials, or provider setup. -->

---

# The client does not import the server function

```text
client: initialize → discover → call tool
server: authorise → validate → read or deny → audit
```

MCP traffic uses stdout; observability belongs on a separate channel.

<!-- Timing: 2 minutes. This prevents the common misunderstanding that a function call proves MCP. The client starts a separate server process and speaks the protocol over stdio. -->

---

# Permit, deny, and prove it with a live MCP call

Sources: `m12_governed_mcp/04_governed_chronos_server.py` · `05_permit_deny_prove.py`

```python
await session.initialize()
tools = await session.list_tools()

allowed = await session.call_tool("advisor_client_review", {"client_id": "alice"})
denied = await session.call_tool("advisor_client_review", {"client_id": "bob"})
```

```text
Discovered: ['advisor_client_review']
ALLOW: ... downstream_executed: true
DENY:  ... unassigned_client ... downstream_executed: false
```

<!-- Timing: 7 minutes. Run `uv run python m12_governed_mcp/05_permit_deny_prove.py` from CODEALONGS. Narrate only the client loop: initialize, list, call Alice, call Bob. Inspect returned JSON and server stderr. This is the live proof: a separate MCP server permits a bounded read, denies an unassigned request before data access, and emits audit evidence. -->

---

# An audit event proves a policy decision

```json
{
  "correlation_id": "63081ea0",
  "caller": "advisor_01",
  "tool": "advisor_client_review",
  "decision": "deny",
  "downstream_executed": false
}
```

<!-- Timing: 3 minutes. Use an observed event from the live run, not a promise that logs exist. Explain that correlation joins the model run, MCP request, data access, and any later approval record. -->

---

# Audit the decision, not the portfolio

```text
Record: caller, tool, validated request, decision, outcome, duration
Do not record: secrets, a full portfolio, or an unneeded tool result
```

A denial that logs private data has not contained the request.

<!-- Timing: 2 minutes. Ask why logging Bob's portfolio would defeat the denial. The classroom audit is deliberately small and in-memory; a durable protected audit sink is later application work. -->

---

# Consequential work becomes an approval request

Source: `m12_governed_mcp/06_approval_required.py`

```text
read       → bounded facts may be returned
draft      → may remain pending review
delivery / mutation → requires a durable human workflow
```

<!-- Timing: 3 minutes. Run the snippet. Classify capabilities by blast radius. This is a later learner-built Chronos extension, not a baseline capstone feature: M12 establishes the boundary that a future draft, delivery, or mutation must not bypass. -->

---

# The final walkthrough assembles the small controls

Sources: `m12_governed_mcp/07_complete_governed_server.py` · `08_complete_walkthrough.py`

```text
discover approved tools
→ allow Alice's bounded review
→ deny Bob before reading
→ inspect a correlated audit event for each decision
```

The standalone walkthrough also illustrates a later pending-note boundary.

<!-- Timing: 5 minutes. Run the final walkthrough rather than reading all 57 lines first. Let students name which rule produced each line of output. Then trace only the order: caller fixture, scope check, validation, bounded data access, record, and the separate approval concept. -->

---

# M12 governs the MCP boundary; it is not all application security

```text
M12: MCP caller, tool admission, server policy, bounds, audit

M13: deterministic tests + behavioural evaluation
M14: attack resistance and containment
M15: traces, deployment, operational ownership
```

<!-- Timing: 4 minutes. Prevent scope confusion. M12 adds controls closest to an MCP request. M13–M15 reuse the seams across the full product. End by setting the lab goal: prove that an unsafe request cannot reach a record. -->

---

# Lab handoff · Build one governed read boundary

1. Run the supplied local MCP client.
2. Add server-side scope authorisation before the read.
3. Add a `max_positions` validation bound.
4. Record permit and denial audit events.
5. Use the progress checker to prove all three outcomes.

Exit: explain why the unassigned request never reaches the data service.

<!-- Timing: 4 minutes. Point learners to `SLIDES-markdown/m12-lab-instructions.md` and `CODEALONGS/m12_governed_mcp/lab/README.md`. They should work in pairs: one navigates the starter, one predicts evidence before running it. The goal is a crisp, observable policy boundary—not a full production authentication solution. The capstone extension uses the same progression with actual Chronos portfolio facts. -->
