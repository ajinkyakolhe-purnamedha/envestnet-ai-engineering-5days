---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M10 · MCP Fundamentals

Your advisor agent already has useful tools.

Today, make those tools available to another AI application.

**MCP means Model Context Protocol:** a shared way for applications to find and call tools.

By the end, you can:

- explain why MCP exists
- build a small MCP server
- discover and call its tools
- reuse the same tools in two applications

<!-- MCP is the next step after the checkpoint lab. It does not replace the agent, RAG, or the local model. It helps another application use the same useful Python capabilities. Keep the question simple: how can two applications use the same trusted tool without sharing all of their code? -->

---

<!-- _class: lead -->

# M10.1 · The Tool Is Stuck Inside One App

The checkpoint advisor calls Python functions directly:

```text
advisor agent
  -> portfolio_summary("alice")
  -> policy_rag("concentration limit")
```

They work — but only inside that application.

<!-- The functions are useful, but the investor chat or a future advisor workspace cannot use them without importing Chronos code. That means each new application must learn private file paths and setup details. The problem is not that the agent is weak. The problem is that a useful tool is trapped inside one app. -->

---

# M10.1.2 · We Want to Share a Tool, Not an App

Bad sharing:

```text
new app -> imports Chronos internals
```

Better sharing:

```text
new app -> asks Chronos for a portfolio summary
```

The second option shares a clear job.

<!-- A clear job is easier to reuse and safer to reason about. “Give me Alice's portfolio summary” is a narrow request. “Import our whole advisor application” is not. MCP helps an application offer clear jobs to other applications. -->

---

# M10.1.3 · The Question MCP Answers

> How can Chronos offer useful tools without sharing its whole codebase?

Not by giving the model:

- database credentials
- a Python console
- a copy of every internal function

<!-- Let students answer before introducing MCP. We need a small, named interface: the caller can see what is available, send valid inputs, and receive a result. Chronos keeps control of the code and data behind that interface. -->

---

<!-- _class: lead -->

# M10.2 · MCP Connects Apps to Tools

Before MCP:

```text
agent -> local Python function
```

With MCP:

```text
application -> MCP client -> MCP server -> Python function
```

MCP changes how the function is reached.

<!-- The portfolio calculation and policy search are still normal Python. MCP does not move intelligence into the server. It creates a clear door through which another application can ask to use those functions. -->

---

# M10.2.2 · What an MCP Client Can Do

An MCP client can ask:

1. What tools do you offer?
2. What inputs does each tool need?
3. Call this tool with these inputs.
4. What result did it return?

<!-- This is the whole behaviour to remember today: discover, understand, call, and read the result. The client does not need to import the server's Python file. We will see each step in the Chronos client output. -->

---

# M10.2.3 · What MCP Does Not Do

MCP does not:

- make a model smarter
- choose tools for the model
- decide who has permission
- make data safe by itself

MCP is a connection and tool-sharing standard.

<!-- A tool description is not permission. The application still decides which tools an agent may see, and the server must still check important rules. We use safe demo data today. Later modules cover what data an agent should receive and how to enforce access rules. -->

---

<!-- _class: lead -->

# M10.3 · Build a Small Chronos Server

Publish two read-only tools:

```text
portfolio_summary(client_id)
search_policy(query)
```

Code: `checkpoint_chronos_advisor/mcp_extension/server.py`

<!-- These are deliberately small tools. One returns a demo portfolio. One searches the investment policy. There is no trading tool, database console, or LLM inside the server. Starting small makes the boundary easy to see. -->

---

# M10.3.2 · A Tool Tells Clients How to Use It

```python
@mcp.tool()
def portfolio_summary(client_id: str) -> dict:
    """Return the simulated portfolio for one Chronos investor."""
```

- name: `portfolio_summary`
- input: `client_id`
- result: a portfolio dictionary

<!-- The decorator makes this function visible to MCP clients. The name, input type, docstring, and returned result help a client understand the tool. Think of this as a small promise: if you send a client ID, Chronos will return this kind of result. -->

---

# M10.3.3 · The Server Runs Separately

```text
client.py  -- stdio -->  server.py
                          -> portfolio code
                          -> policy code
```

The client does not import the server function.

<!-- In this lab, stdio means the client starts the server as a separate local program and talks through standard input and output. This proves that the client is using a real boundary, not a hidden Python import. A remote server changes where it runs, not these three roles. -->

---

<!-- _class: lead -->

# M10.4 · Connect, Discover, Call

The client does this in order:

```text
start server -> connect -> list tools -> call a tool
```

Run: `checkpoint_chronos_advisor/mcp_extension/client.py`

<!-- Run the client now. Read the output in order. Listing tools is important: it shows that the client learned what the server offers instead of assuming a Python function exists in a particular file. -->

---

# M10.4.2 · Three Roles

| Role | Chronos example | Main job |
| --- | --- | --- |
| host | investor or advisor app | works with the user |
| client | MCP code in that app | talks to the server |
| server | Chronos tool program | runs the tools |

The model can be inside the host. It is not the client.

<!-- Use these names carefully. The host is the application the user sees. It may contain an LLM agent. The client is ordinary application code that opens the MCP connection. The server owns the tools. This avoids the vague statement “the model uses MCP”; the application uses MCP and may give results to the model. -->

---

# M10.4.3 · Discovery Is the Important New Step

```text
Discovered tools:
['portfolio_summary', 'search_policy']
```

Then the client can call:

```text
portfolio_summary("alice")
search_policy("concentration limit")
```

<!-- Discovery means asking the server what it offers before calling a tool. The names and inputs come from the server, not from an import statement. A different application can perform the same discovery and use the same two tools. -->

---

# M10.4.4 · Tools, Resources, and Prompts

| Type | Use it when | Chronos example |
| --- | --- | --- |
| tool | you need to do a job with inputs | portfolio summary for Alice |
| resource | you need a named piece of context | investment policy document |
| prompt | you need a reusable writing pattern | advisor meeting brief |

Today we build tools.

<!-- Do not call every shared item a tool. A tool does a job and usually takes inputs. A resource is something to read at a known location. A prompt is reusable wording. The policy search is a tool because the client sends a query; the full policy could also be offered as a resource later. -->

---

<!-- _class: lead -->

# M10.5 · One Server, Two AI Applications

```text
                Chronos MCP server
         / portfolio_summary + search_policy \
Investor Education Agent          Advisor Preparation Agent
```

Same tools. Different applications.

<!-- This is the reason MCP is useful. We are not moving one agent to another place. We are letting two different applications ask the same trusted server for the same narrow facts. Each application can still have its own prompt, user, and output. -->

---

# M10.5.2 · Investor Education Agent

Question:

> “Explain diversification and the concentration policy in plain language.”

- calls the portfolio tool
- calls the policy tool
- uses the local model to explain the results
- does not trade or give a personal recommendation

Code: `mcp_extension/investor_agent.py`

<!-- Trace the flow. The investor app calls the live MCP tools first. It then gives the returned facts and policy evidence to the local model for a readable explanation. Python gets the facts; the model explains them. The tool result is not an instruction to trade. -->

---

# M10.5.3 · Advisor Preparation Agent

Question:

> “Prepare an internal portfolio-review meeting brief.”

- calls the same two tools
- uses a different prompt
- writes for an advisor, not an investor
- produces a draft for review

Code: `mcp_extension/advisor_agent.py`

<!-- This application receives the same trusted facts but has a different job. Its output is an internal draft, not a client explanation. The small local model may write a plain answer; that is okay. Good writing quality and reusable tool access are separate things to evaluate. -->

---

# M10.5.4 · The Reuse Lesson

```text
same MCP tools
does not mean same agent
does not mean same prompt
does not mean same user experience
does not mean same permission
```

MCP shares tools, not an entire agent.

<!-- Ask for another possible user of these tools: support, reporting, compliance review, or a test program. It may use the same server but should still have its own purpose and permissions. Reuse is valuable because the shared part is small and clear. -->

---

<!-- _class: lead -->

# M10.6 · A Tool Boundary Is Not Enough for Production

M10 proves:

```text
publish -> discover -> call -> reuse
```

It does not yet answer:

```text
who may call? which data? how much? what was recorded?
```

<!-- This demo uses read-only classroom data, so it is safe for learning. A real enterprise server still needs to know who is calling, what that person may access, what input is valid, how often it may be called, and what happened. MCP gives us a useful place to add those checks; it does not add them automatically. -->

---

# M10.6.2 · What Comes Next

| Module | Next question |
| --- | --- |
| M11 | What small, useful data should an agent receive? |
| M12 | How do we check identity, access, limits, and logs? |

Closing question:

> Which Chronos tools should be shared, and which should stay inside one app?

<!-- Do not conclude that MCP is needed for every helper function. Direct Python is still a good choice when a helper belongs to one small application. MCP is useful when a capability should be found and reused by more than one host. The next modules make that shared boundary narrower and safer. -->

---

<!-- _class: lead -->

# Lab · Publish, Discover, Reuse

1. Run the Chronos MCP client and read the discovered tools.
2. Improve one tool description or result shape.
3. Run the investor and advisor applications against the same server.
4. Explain why they share tools but not behaviour or permission.

Exit: trace one request from app → client → server → tool result → app output.

<!-- Keep the lab small. The learner should be able to point to where the request starts, where the tool runs, and where the result is used. Do not add login, database access, or write actions today. Those are later engineering problems; this lab is about understanding the basic connection and reuse pattern. -->
