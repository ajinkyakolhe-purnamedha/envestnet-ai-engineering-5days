---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M10 · MCP Fundamentals

LLMs can generate useful responses.

Applications need a safe way to use real tools and data.

**MCP = Model Context Protocol**

<!-- Start with the general problem, not Chronos. An LLM can write an answer about a portfolio, but it cannot automatically read a company portfolio or search an internal policy. The application around the model must connect to those capabilities. -->

---

# M10.1 · Models Generate. Applications Use Systems.

```text
LLM: “I can explain a portfolio.”

Application: “I can read this portfolio and search this policy.”
```

The model does not automatically have access to your systems.

<!-- Keep the distinction simple. Models generate responses. Applications call databases, services, files, and tools. The application decides what the model may use and how it reaches those systems. -->

---

# M10.1.2 · Before MCP, Every Connection Is Custom

```text
AI App A -> its connector -> portfolio data
AI App B -> another connector -> portfolio data
AI App C -> another connector -> portfolio data
```

Each application learns its own way to reach the same capability.

<!-- A custom connection may be perfectly sensible for one small application. The problem appears when several applications need the same business capability. Each connection has its own code, setup, and assumptions. -->

---

# M10.1.3 · The Same Useful Capability Gets Rebuilt

```text
Investor App -> get portfolio
Advisor App  -> get portfolio
Support App  -> get portfolio
```

We want one clear way to ask for that job.

<!-- The goal is not to share an entire application. It is to share a small business capability, such as “get this portfolio summary.” The caller should not need to learn the private code structure behind the capability. -->

---

# M10.1.4 · We Need a Clear External Capability

```text
input:  client_id
job:    return a portfolio summary
result: cash and holdings
```

This is safer and easier to reuse than giving a model broad system access.

<!-- A useful external capability has a clear input, one job, and a clear result. It is not “run any Python,” “search any database,” or “use every internal API.” This is the shape MCP helps applications share. -->

---

# M10.1.5 · The MCP Idea

```text
AI application  ->  MCP  ->  tools and data
```

> MCP is a shared way for applications to find and call external capabilities.

<!-- This is the definition to remember. MCP gives applications shared connection rules: ask what is available, understand how to call it, make a request, and receive a result. The server still owns the code and data behind the capability. -->

---

<!-- _class: lead -->

# M10.2 · The MCP Loop

```text
Discover  ->  Understand  ->  Call  ->  Result
```

1. What tools do you offer?
2. What inputs do they need?
3. Run this tool.
4. Here is the result.

<!-- This is the central mental model for the module. The client first discovers what exists, then reads how to call it, makes a request, and receives a result. Students should be able to say this loop before looking at any code. -->

---

# M10.2.2 · The Model Does Not Connect Directly

```text
user
  -> host application
       -> LLM
       -> MCP client -> MCP server -> tool
```

The application owns the connection.

<!-- This corrects a common misunderstanding. The host application contains the LLM and the MCP client. Ordinary application code opens the connection and calls the server. The model may be shown the tools or their results, but it is not itself the network client. -->

---

# M10.2.3 · Name the Roles

| Role | Plain meaning | Example |
| --- | --- | --- |
| host | the app used by a person | an investor app |
| client | code that talks to a server | MCP connection in the app |
| server | program that offers tools | a portfolio server |
| tool | one useful job | get a portfolio summary |

<!-- Use general examples here. A host is the application the user interacts with. Its client talks to an MCP server. The server offers tools. We will map these roles to Chronos only after students understand the general picture. -->

---

# M10.2.4 · What Does a Tool Exchange Look Like?

```text
Client: What tools do you have?

Server: portfolio_summary
        input: client_id
        returns: cash and holdings
```

```text
Client: portfolio_summary(client_id="alice")

Server: {cash: 25000, holdings: [SPY, QQQ, GLD]}
```

<!-- MCP becomes less abstract when students can see the request and result. The server describes a tool, the client sends named inputs, and the server returns data. The exact format is handled by the MCP library; the important design work is choosing a clear name, input, and result. -->

---

# M10.2.5 · MCP Has More Than Tools

| MCP item | Think | Example |
| --- | --- | --- |
| tool | do something | get a portfolio |
| resource | read something | policy document |
| prompt | reuse wording | meeting brief |

Today we focus on tools.

<!-- A tool does a job and usually takes inputs. A resource is named context that can be read. A prompt is reusable wording. Today we focus on tools, because they make the connection pattern easiest to see. -->

---

# M10.2.6 · MCP and Function Calling Work Together

```text
Function calling:
agent -> tools registered inside one application

MCP:
application -> tools offered by another program
```

MCP can supply tools that an agent later uses through function calling.

<!-- Do not teach these as competitors. In earlier modules, the agent was given locally registered functions. With MCP, the host can discover external tools and decide whether to offer them to an agent. MCP makes the connection reusable; function calling is one way an agent can choose among available tools. -->

---

<!-- _class: lead -->

# M10.3 · Now Return to Chronos

In M7–M9, the Chronos Advisor App registered local Python tools:

```text
portfolio_summary()
policy_rag()
```

That was the right design for one custom agent.

<!-- Now map the general idea back to the course. Students already built a custom agent by registering local functions. We are not saying that design was wrong. We are asking what changes when another application needs the same trusted capability. -->

---

# M10.3.2 · Without MCP, Apps Share Internals

```text
Advisor App
  -> imports and registers local functions

Investor App
  -> must repeat the connection
```

The second app becomes tied to Chronos implementation details.

<!-- The investor app should need to know what a portfolio summary is, not where Chronos stores the function or how it sets up its dependencies. It might import internal files, copy a connector, or build a different one. Either way, the connection is repeated. -->

---

# M10.3.3 · The Second App Needs the Same Facts

```text
Investor Education App:
“Explain diversification in plain language.”

Advisor Preparation App:
“Prepare an internal meeting brief.”
```

Both need a portfolio summary and policy evidence.

<!-- The two applications have different users and different outputs. Their shared need is narrower: trusted portfolio facts and policy evidence. This is exactly the kind of capability that should be reusable without sharing an entire agent. -->

---

# M10.3.4 · With MCP, Apps Share Capabilities

```text
Investor App ---\
Advisor App ----- > Chronos MCP Server
Support App  ---/       -> portfolio_summary
                         -> search_policy
```

> We share capabilities, not the application.

<!-- This is the module’s key sentence. Each application can ask the Chronos server for the same narrow capability. The server keeps the Python implementation private. The applications do not become the same application, and they do not automatically receive the same permissions. -->

---

<!-- _class: lead -->

# M10.4 · Build the Chronos MCP Server

```python
@mcp.tool()
def portfolio_summary(client_id: str) -> dict:
    """Return a simulated investor portfolio."""
```

Code: `m10_mcp_fundamentals/02_chronos_mcp_server.py`

<!-- This is the first implementation step. The decorator publishes an ordinary Python function as an MCP tool. Its name, input type, docstring, and result help clients understand how to use it. The business logic remains ordinary Python. -->

---

# M10.4.2 · A Tool Is a Small Promise

```text
name: portfolio_summary
input: client_id
result: cash and holdings
```

Make each tool:

- narrow
- clear
- read-only for this lab

<!-- A tool is a promise between server and client. A good tool has one understandable job, clear inputs, and a predictable result. We do not publish “run any Python,” “query any database,” or trading actions. Starting narrow makes reuse and later governance easier. -->

---

# M10.4.3 · The Server Runs as a Separate Program

```text
client.py  -- stdio -->  server.py
                          -> portfolio code
                          -> policy code
```

The client does not import the server function.

<!-- In this lab, stdio means the client starts the server as a separate local program and communicates through standard input and output. This makes the boundary real: the client asks the server to run a tool instead of importing its Python function. -->

---

# M10.4.4 · The Client Follows the MCP Loop

```python
await session.initialize()
tools = await session.list_tools()
result = await session.call_tool(
    "portfolio_summary", {"client_id": "alice"}
)
```

Code: `m10_mcp_fundamentals/03_discover_and_call.py`

<!-- Read this in the order students learned: connect, discover, understand, call, result. The client library handles the connection details. The code makes the core MCP loop visible in only a few lines. -->

---

# M10.4.5 · Discovery Is the New Step

```text
Discovered tools:
['portfolio_summary', 'search_policy']
```

The client learns what the server offers before it calls a tool.

<!-- Discovery removes the direct-import assumption. A host can ask the server which tools it has rather than relying on a known local file. In a real application, the host can then decide which discovered tools are appropriate to expose to an agent. -->

---

<!-- _class: lead -->

# M10.5 · One Server, Two Applications

```text
                Chronos MCP Server
         / portfolio_summary + search_policy \
Investor Education App          Advisor Preparation App
```

Same tools. Different jobs.

<!-- This proves the value of the boundary. One server offers trusted portfolio and policy capabilities. Each host uses them for a different user and a different outcome. -->

---

# M10.5.2 · Investor Education App

```text
Question: Explain diversification in plain language.

1. call portfolio tool
2. call policy tool
3. let the local model explain the results
```

It does not trade or make a personal recommendation.

<!-- The investor application uses live MCP tool results as facts. The local model turns those facts into a readable educational explanation. Python retrieves and controls; the model explains. -->

---

# M10.5.3 · Advisor Preparation App

```text
Question: Prepare an internal meeting brief.

1. call the same portfolio tool
2. call the same policy tool
3. draft a brief for advisor review
```

Same facts. Different audience and output.

<!-- The advisor application uses the same server but has a different purpose. It produces an internal draft, not a client answer. This shows why sharing tools does not mean sharing behaviour, prompts, or authority. -->

---

<!-- _class: lead -->

# M10.6 · MCP Is Not the Whole Safety Story

M10 proves:

```text
publish -> discover -> call -> reuse
```

It does not yet answer:

```text
who may call? which data? how much? what was recorded?
```

<!-- This server uses read-only demo data, so it is safe for a classroom. In a real enterprise system, the server must still check identity, access, inputs, limits, and logs. MCP gives us a useful boundary for those checks; it does not add them by itself. -->

---

# Lab · Publish, Discover, Reuse

1. Run the server and client cards.
2. Inspect the tools the client discovers.
3. Add or improve one small read-only tool.
4. Run the investor and advisor apps against the same server.

Exit: explain how a local custom-agent tool became a reusable MCP tool.

<!-- The lab proves the whole story: the earlier agent had local functions; the MCP server publishes those capabilities; another application discovers and calls them; two hosts reuse them differently. M11 and M12 will make this boundary more governed and secure. -->
