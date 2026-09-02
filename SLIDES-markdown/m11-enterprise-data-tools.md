---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M11 · Connecting to Enterprise Data and Tools

First: a fast, functional MCP revision.

Then: design MCP capabilities for real enterprise data.

<!-- Timing: 1 minute. M11 deliberately begins with a compact M10 refresh so every learner has the same mental model before the data-design material begins. -->

---

<!-- _class: lead -->

# Part 1 · MCP in Six Minutes

```text
application needs a capability
→ MCP lets it discover and call a separate provider of that capability
```

<!-- Timing: 1 minute. This is a revision, not a second M10. Tell learners they should be able to trace this loop before moving on. -->

---

# 1 · Why MCP Exists

Without MCP:

```text
each AI application imports or rebuilds its own connector
```

With MCP:

```text
many applications discover and call one published capability
```

MCP shares a capability—not an entire agent or its authority.

<!-- Timing: 1 minute. Reconnect to M10’s coupling problem. We do not share an app, a prompt, or a database connection. We share a small, named operation. -->

---

# 2 · The Four Roles and One Loop

```text
user → host application
          ├─ model
          └─ MCP client → MCP server → tool
```

```text
discover → understand inputs → call → receive result
```

The application owns the connection and decides what the model sees.

<!-- Timing: 2 minutes. Name the roles: host is the user-facing app; client is protocol code in the host; server offers capabilities; a tool does one parameterised job. The model is not the network client. -->

---

# 3 · MCP Primitives and Function Calling

| MCP item | Purpose | Example |
| --- | --- | --- |
| tool | parameterised work | get a portfolio view |
| resource | addressable read context | policy document |
| prompt | reusable wording | meeting-brief template |

Function calling helps a model select a tool. MCP supplies reusable external tools.

<!-- Timing: 1 minute. Do not present MCP and function calling as alternatives. An application can discover MCP tools and offer an approved subset to a model through function calling. -->

---

# 4 · What MCP Does *Not* Do

MCP does not decide:

```text
who may call a tool
which data they may see
how much data may return
whether a request is safe
```

M11 designs the capability. M12 enforces identity, policy, and audit.

<!-- Timing: 1 minute. This is the bridge to M11. MCP provides a useful boundary, but a boundary with the wrong capability behind it is still a problem. -->

---

<!-- _class: lead -->

# Part 2 · The Enterprise Data Problem

The question is not “can the agent query our database?”

> It is “what smallest business question should it be able to answer?”

<!-- Timing: 1 minute. Switch from protocol mechanics to capability design. -->

---

# 5 · Raw Access Is Not a Business Capability

```text
agent → database → any table → any row
agent → vendor API → any endpoint → any parameter
```

An advisor does not need SQL, schemas, joins, or an API catalogue.

It needs a useful fact.

<!-- Timing: 3 minutes. Raw access exposes storage details, produces arbitrary results, creates cost and risk problems, and couples callers to implementation. -->

---

# 6 · Curated Data Product

```text
raw source → curated data product → MCP tool → application
```

```text
investor_portfolio_view(client_id, max_positions)
  → cash, holdings, simulated_date, source
```

> Share the answerable business question, not the storage mechanism.

<!-- Timing: 3 minutes. The source can later change from a read replica to an API without changing the tool’s business contract. -->

---

# 7 · Match the Capability to the Question

| Question | Correct capability |
| --- | --- |
| Portfolio return over a period? | bounded query/aggregation |
| Policy support for a claim? | retrieval with evidence |
| Latest approved price? | market-data service |

RAG retrieves text. It does not calculate current structured facts.

<!-- Timing: 3 minutes. Connect this to prior modules. Explain that an LLM should neither invent a total nor infer it from document fragments. -->

---

# 8 · The Contract Is the Product

```text
question: What is this investor's small portfolio view?
input:    client_id, max_positions ≤ 3
result:   cash, top positions, as_of, source
absence:  controlled not_found result
```

Bounds belong in deterministic Python, never only in a prompt.

<!-- Timing: 3 minutes. A good contract has small named inputs, predictable output, explicit bounds, provenance, and a controlled absence path. -->

---

# 9 · Enterprise Read Path

```text
MCP server → curated read model / approved service
           → read replica, warehouse view, or governed API
```

Prerequisites: read-only access, least privilege, result limits, source, and freshness.

<!-- Timing: 3 minutes. M11 describes the safe data-product shape. Short-lived credentials, caller identity, server-side authorization, and audit are the M12 implementation problem. -->

---

<!-- _class: lead -->

# Part 3 · Learn the Pattern in a Tiny Chronos

```text
ordinary Python data product
→ MCP tool
→ live result
→ trusted model context
→ explanation or internal draft
```

<!-- Timing: 1 minute. Only after the concept is established do we open the small runnable code. -->

---

# 10 · Card 1: Small, Governed Facts

Source: `01_curated_data_product.py`

```python
build_current_portfolio_snapshot("alice", max_positions=2)
generate_advisor_review_report("alice")
```

The card shows a bounded result, provenance, truthful absence, and deterministic rejection.

<!-- Timing: 5 minutes. Run it. The miniature data is deliberately simple so the class can focus on the contract rather than a database schema. -->

---

# 11 · Card 2: Publish Only the Contracts

Source: `02_chronos_data_server.py`

```python
@mcp.tool()
def investor_portfolio_view(client_id: str, max_positions: int = 3) -> dict: ...

@mcp.tool()
def advisor_client_review(client_id: str) -> dict: ...
```

No raw SQL. No generic API proxy. No write tool.

<!-- Timing: 3 minutes. This is the M10 decorator applied to a properly designed enterprise capability. -->

---

# 12 · Card 3: Real MCP Calls, Real Model Call

Source: `03_explain_live_governed_facts.py`

```python
facts = await session.call_tool("investor_portfolio_view", {...})
reply = generate(investor_messages(facts.content[0].text))

# --audience advisor calls advisor_client_review and produces a pending draft
```

The local model receives live MCP JSON. There is no canned answer.

<!-- Timing: 7 minutes. Run the full card. The application retrieves governed facts, chooses exactly what the model can see, then uses the real local model for natural-language explanation. -->

---

<!-- _class: lead -->

# Part 4 · Now Map the Pattern to Chronos

The miniature code taught the pattern.

The capstone is the real system where the lab applies it.

<!-- Timing: 1 minute. This is the intentional transition. Do not teach the capstone internals before the MCP/data-product pattern is understood. -->

---

# 13 · Chronos Keystone Architecture

```text
demo login
  ├─ Alice Investor → investor dashboard → own portfolio + education
  └─ Demo Advisor   → advisor dashboard  → client review + draft approval

FastAPI routes → deterministic Chronos services → portfolio / prices / draft state
```

M11 adds a curated MCP boundary around selected deterministic capabilities.

<!-- Timing: 4 minutes. This is an architecture orientation slide, not a code walkthrough. The capstone already has demo personas, role-specific dashboards, deterministic finance services, an advisor assistant, and an approval queue. -->

---

# 14 · Same Facts, Different Product Features

| Logged-in experience | Uses facts for | Output boundary |
| --- | --- | --- |
| Investor | understand their own portfolio | education, no trade advice |
| Advisor | review a selected client | internal draft, human approval |

They share deterministic facts—not prompts, authority, or outcomes.

<!-- Timing: 3 minutes. This makes the product reason for MCP/data products tangible. It also sets up why M12 must enforce authority rather than trusting role text in a prompt. -->

---

# 15 · Miniature-to-Capstone Mapping

| Miniature lesson | Capstone equivalent |
| --- | --- |
| miniature snapshot service | `build_current_portfolio_snapshot()` |
| miniature review service | `analyze_client_portfolio()` and `generate_advisor_review_report()` |
| explanation from facts | advisor assistant runtime |
| controlled output boundary | draft and approval queue |

The lab replaces the small simulated functions with these real services.

<!-- Timing: 4 minutes. Show the function names and files, but do not read their hundreds of lines. Students need a map for the lab, not a second lecture on FastAPI or SQLAlchemy. -->

---

# Lab 11 · Apply the Pattern to the Capstone

1. Locate the real deterministic portfolio and advisor-review functions.
2. Define narrow MCP tool contracts around them.
3. Build investor and advisor agent flows from live tool results.
4. Preserve the advisor draft-and-approval boundary.

Exit: explain why the tiny snippets and the real capstone use the same pattern.

<!-- Timing: 2 minutes. The lab uses the real application; it does not recreate its database, dashboards, or finance calculations. M12 then hardens the new MCP boundary with server-side security and audit controls. -->

---

# M11 Exit → M12

```text
M11: useful contract + bounded result + provenance + safe read path

M12: identity + authorisation + allowlists + resource policy + audit + safe failure
```

<!-- Timing: 1 minute. Close with a crisp boundary. Students have learned how to make an enterprise capability useful and small. The next module determines who may use it and proves overreach is stopped. -->
