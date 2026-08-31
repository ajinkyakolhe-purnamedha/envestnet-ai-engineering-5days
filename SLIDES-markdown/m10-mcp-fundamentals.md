---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M10 · MCP Fundamentals

Your advisor agent already has tools.

Today, publish those tools so another AI application can discover and use them.

By the end of this module you can:

- explain why MCP exists
- build a read-only MCP server
- discover and call tools from a separate client
- reuse the same capabilities in two AI applications

<!-- Start from the familiar checkpoint assistant. This is not a new agent framework or a replacement for RAG. It is the next integration boundary. Point out that participants have already written the two capabilities we will publish. -->

---

<!-- _class: lead -->

# M10.1 · Your Agent Works — In One Process

The checkpoint advisor has direct Python tools:

```text
advisor agent
  -> portfolio_summary("alice")
  -> policy_rag("concentration limit")
```

They are useful.

They are also trapped inside this application.

<!-- Ask what happens if the investor chat, a future advisor workspace, or another host wants the same portfolio capability. Today they would import Chronos code, learn its internal layout, and duplicate setup. The problem is coupling, not an LLM failure. -->

---

# M10.1.2 · The Coupling Problem

```text
one agent imports one function
        ↓
another application imports it differently
        ↓
shared capability becomes shared internals
```

We want to share a capability — not an application codebase.

<!-- Emphasise the difference between reusing an answer and reusing a capability. We want a stable business-shaped interface: give a client identifier, receive a portfolio summary. -->

---

# M10.1.3 · The Question MCP Answers

> How can Chronos publish useful capabilities without publishing its whole agent application?

Not:

- give the model database credentials
- copy the function into every agent
- expose a generic Python or SQL console

<!-- Let learners predict the desirable answer: a narrow, discoverable, reusable interface. This sets up MCP as an integration protocol, not an AI feature. -->

---

<!-- _class: lead -->

# M10.2 · MCP Publishes Capabilities

Before MCP:

```text
agent -> local Python function
```

With MCP:

```text
host/client -> MCP server -> existing Python function
```

<!-- Say the important sentence slowly: MCP changes the boundary, not the business logic. The portfolio calculation and policy search remain ordinary deterministic Python behind the server. -->

---

# M10.2.2 · What MCP Standardises

An MCP client can ask a server:

- what tools do you provide?
- what arguments does each tool accept?
- call this tool with these arguments
- what result did it return?

The host no longer needs to import server code.

<!-- Avoid protocol-message detail for now. Learners should recognise the behavior: discovery, schema, call, result. We will see each in the client output. -->

---

# M10.2.3 · What MCP Does *Not* Do

MCP does **not**:

- make a model smarter
- decide which tool the agent should use
- authorise a request
- make unsafe data access safe

It standardises connection and capability discovery.

<!-- This is a crucial boundary. The existing agent decides whether it needs portfolio or policy information. M11 and M12 will add data-product and governance controls. Do not let students infer that a tool description equals permission. -->

---

<!-- _class: lead -->

# M10.3 · Build the Smallest Chronos Server

Publish two read-only tools:

```text
portfolio_summary(client_id)
search_policy(query)
```

They are the same business capabilities the checkpoint agent already uses.

Code: `checkpoint_chronos_advisor/mcp_extension/server.py`

<!-- Before running code, say that each tool remains intentionally narrow. There is no trade execution, no generic query mechanism, and no LLM inside the server. -->

---

# M10.3.2 · A Tool Is a Contract

```python
@mcp.tool()
def portfolio_summary(client_id: str) -> dict:
    """Return the simulated portfolio for one Chronos investor."""
```

The name, docstring, argument, and result are published to clients.

<!-- Point at every part: decorator exposes it; name is what the client discovers; type/docstring make the input understandable; returned dictionary is the result contract. This is why tool design is product design. -->

---

# M10.3.3 · The Server Is a Separate Process

```text
client.py  -- stdio -->  server.py
                          -> portfolio Python
                          -> policy Python
```

The client calls a protocol boundary.

It does not import `portfolio_summary` from `server.py`.

<!-- This is the physical proof of the abstraction. Stdio is the simplest local transport: the client starts the process and communicates over standard input/output. Remote transports change deployment, not the core client/server roles. -->

---

<!-- _class: lead -->

# M10.4 · Connect, Discover, Call

The client lifecycle:

```text
start server -> connect -> initialize -> list tools -> call tool
```

Run: `checkpoint_chronos_advisor/mcp_extension/client.py`

<!-- Ask learners to run the client now. Tell them not to skip the list-tools output: discovery is the behavior that removes the direct-import coupling. -->

---

# M10.4.2 · Name the Three Roles

| Role | Chronos example | Owns |
| --- | --- | --- |
| host | investor or advisor application | user experience, agent workflow |
| client | MCP connection in that application | protocol requests |
| server | Chronos tool process | published capabilities, execution |

The model is not the MCP client.

<!-- A host can contain an LLM agent, but it owns the client. This distinction prevents the vague claim that the model ‘uses MCP’. The application opens the connection and decides what it exposes to the model. -->

---

# M10.4.3 · Discovery Is Visible Evidence

```text
Discovered tools:
['portfolio_summary', 'search_policy']
```

Then the client calls each tool:

```text
portfolio_summary("alice")
search_policy("concentration limit")
```

<!-- Connect visible output to the earlier promise. Another application can now learn the tool names and contracts from the server rather than importing the agent package. -->

---

# M10.4.4 · Tools, Resources, Prompts

| Primitive | Best for | Chronos example |
| --- | --- | --- |
| tool | parameterised operation | `portfolio_summary(client_id)` |
| resource | addressable read context | policy document URI |
| prompt | reusable interaction template | advisor meeting brief |

Start with tools: this module answers parameterised questions.

<!-- Do not build all three today. Learners need the distinction so they do not call everything a tool. A policy document may become a resource later; a prompt never replaces system policy or authorisation. -->

---

<!-- _class: lead -->

# M10.5 · One Server, Two AI Applications

```text
                Chronos MCP server
         / portfolio_summary + search_policy \
Investor Education Agent          Advisor Preparation Agent
```

The server publishes capabilities.

Each application chooses its own workflow and output.

<!-- This is the payoff. MCP is not about moving one agent somewhere else. It makes the business capabilities reusable by applications that have different users, prompts, and success criteria. -->

---

# M10.5.2 · Investor Education Agent

Uses live MCP results to answer:

> “Explain diversification and the concentration policy in plain language.”

- portfolio facts from `portfolio_summary`
- policy evidence from `search_policy`
- local model produces an educational explanation
- no trade or personalised recommendation

Code: `mcp_extension/investor_agent.py`

<!-- Run this example. The tool calls are live MCP calls; the local model only turns returned facts into a readable explanation. This mirrors the course rule: Python retrieves and controls; AI explains. -->

---

# M10.5.3 · Advisor Preparation Agent

Uses the same live MCP results to answer:

> “Prepare an internal portfolio-review meeting brief.”

- same portfolio tool
- same policy tool
- different prompt and audience
- draft requires advisor review

Code: `mcp_extension/advisor_agent.py`

<!-- Contrast it explicitly with the investor agent. Do not focus on whether the 135M output is elegant; use its limitations as evidence that output quality is separate from reusable data/tool integration. -->

---

# M10.5.4 · The Reuse Lesson

```text
same MCP tools
≠ same agent
≠ same prompt
≠ same user experience
≠ same authority
```

MCP reuses capabilities, not one agent's behaviour.

<!-- Ask learners to name a second internal application that could use these two tools: reporting, support, compliance review, or a test harness. The server is reusable precisely because its capability contract is narrow. -->

---

<!-- _class: lead -->

# M10.6 · The Boundary Is Not Governance

M10 proved:

```text
publish -> discover -> call -> reuse
```

It has not yet proved:

```text
who may call -> which data -> how much -> audit what happened
```

<!-- This is the honest handoff. The server is deliberately read-only and uses demo data, but it is not an enterprise governance implementation. Do not let the local demo imply production readiness. -->

---

# M10.6.2 · What Comes Next

| Module | Next question |
| --- | --- |
| M11 | What narrow data product should an agent receive? |
| M12 | How does the server enforce identity, scope, limits, and audit? |

Closing question:

> Which Chronos capabilities should be shared — and which should remain inside the application?

<!-- End by returning to architecture judgement. MCP earns its complexity when a capability genuinely needs reuse across hosts. If one helper belongs to one small application, direct Python may still be the correct answer. -->

---

<!-- _class: lead -->

# Lab · Publish, Discover, Reuse

1. Run the Chronos MCP client and inspect discovered tools.
2. Add one read-only tool description or improve an existing result contract.
3. Run both the investor and advisor agents against the same server.
4. Explain why they reuse MCP capabilities but do not share behaviour or authority.

Exit: you can trace one request from application → client → server → tool result → application output.

<!-- Keep the lab focused on the M10 thesis. Do not add authentication, raw database access, or write actions; those would introduce M11/M12 machinery before the fundamental client/server boundary is understood. -->
