---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M8 · Agentic Frameworks

From the M7 loop to practical framework code.

This module uses:

- smolagents
- LlamaIndex

By the end of this module you can:

- map framework APIs back to the M7 loop
- define smolagents tools
- wrap Python functions with LlamaIndex
- expose RAG as an agent tool
- build a small end-to-end agentic workflow

---

<!-- _class: lead -->

# M8.1 · From Manual Loop To Framework Runtime

M7 gave us the core pieces:

| M7 code | Framework name |
|---|---|
| `TOOL_FUNCTIONS` | tools |
| `planner(state)` | agent planner |
| `dispatch(step)` | tool runtime |
| `observations` | trace / memory |
| `max_turns` | step limit |

A framework does not remove the loop.

It packages the loop.

---

# M8.1.2 · What To Look For

When reading an agent framework, ask:

- how are tools registered?
- how are tool descriptions generated?
- who validates arguments?
- where is the step limit?
- where is the trace?
- what happens when the model fails to call a tool?

These questions are more important than the framework name.

---

# M8.1.3 · Framework Tradeoff

Frameworks help when they remove repeated runtime code:

- tool metadata
- parsing
- dispatch
- trace events
- retries
- step limits

Frameworks hurt when they hide prompts, tool calls, or stop reasons.

Use a framework only if you can inspect the runtime behavior.

---

# M8.1.4 · Where Did Your Runtime Go?

When you read a framework, find the M7 parts:

| Runtime job | Question to ask |
|---|---|
| tool registry | where are tools allowed? |
| planner | which model chooses the next step? |
| dispatch | who actually calls Python? |
| observation | where do tool results go? |
| step limit | where does the loop stop? |
| trace | how do I replay the run? |

If you cannot find these, you cannot operate the agent.

---

# M8.1.5 · The Case Against Frameworks

Frameworks are not automatically safer.

They can hide:

- prompts
- tool-call parsing
- retries
- stop reasons
- intermediate observations
- token and latency cost

Use a framework for leverage.

Do not use it as a black box.

---

<!-- _class: lead -->

# M8.2 · smolagents Tool Agent

smolagents turns Python functions into model-callable tools:

```python
from smolagents import ToolCallingAgent, tool

@tool
def price_tool(symbol: str) -> dict:
    """Return the simulated current price for one ticker."""
    return get_current_price(symbol)
```

`@tool` uses the function name, type hints, and docstring.

Code: `CODEALONGS/m8_agentic_frameworks/01_smolagents_tool_agent.py`

---

# M8.2.2 · The Agent Shape

```python
agent = ToolCallingAgent(
    tools=[price_tool, guideline_tool],
    model=model,
    max_steps=3,
)
```

Mapping back to M7:

- `tools` is the registry
- `model` is the planner
- `max_steps` is `max_turns`
- framework logs are the trace

---

# M8.2.3 · Trace Limits

Small or weak planners can produce bad tool calls.

Framework trace should show:

- malformed model output
- failed parse
- failed validation
- step count
- controlled stop at `max_steps`

Do not hide these failures.

Teach the trace.

Code: `CODEALONGS/m8_agentic_frameworks/02_smolagents_trace_limits.py`

---

# M8.2.4 · What A Step Costs

Every agent step can add:

- one model call for planning
- tool latency
- larger context from observations
- another model call for the next decision

Loops multiply cost and latency.

`max_steps` is a product and budget control, not just a safety switch.

---

<!-- _class: lead -->

# M8.3 · LlamaIndex Tools And RAG Capabilities

LlamaIndex also wraps Python functions:

```python
from llama_index.core.tools import FunctionTool

price_tool = FunctionTool.from_defaults(fn=get_current_price)
guideline_tool = FunctionTool.from_defaults(fn=check_guideline)
```

The tool is still your Python function.

The framework provides metadata and runtime integration.

Code: `CODEALONGS/m8_agentic_frameworks/03_llamaindex_function_agent.py`

---

# M8.3.2 · FunctionAgent

```python
from llama_index.core.agent.workflow import FunctionAgent

agent = FunctionAgent(
    tools=[price_tool, guideline_tool],
    llm=Settings.llm,
    system_prompt="Use tools before answering.",
)
```

The important design question:

```text
Which functions should this agent be allowed to call?
```

Not every function belongs in the tool list.

---

<!-- _class: lead -->

# M8.3.3 · RAG As An Agent Tool

RAG from M4 can become a tool:

```python
from llama_index.core.tools import QueryEngineTool

policy_tool = QueryEngineTool.from_defaults(
    query_engine=policy_query_engine,
    name="search_policy",
    description="Search the advisor policy manual.",
)
```

Now the agent can ask policy questions during its workflow.

Code: `CODEALONGS/m8_agentic_frameworks/04_llamaindex_rag_tool.py`

---

# M8.3.4 · Tool Mix

An agent can combine:

- data tools: current price
- state tools: current allocation
- policy tools: RAG over policy documents
- calculation tools: guideline check
- writing step: final advisor note

RAG is no longer the whole application.

It is one capability inside the agent.

---

<!-- _class: lead -->

# M8.4 · Agentic Workflow Patterns

Not every agentic app needs full autonomy.

Useful controlled patterns:

```text
routing         choose the workflow
chaining        run known steps in order
parallel gather collect independent facts
evaluator       check or revise the draft
handoff         move to another human/app/agent
```

Most production agentic apps are workflows with model-planned parts.

Not infinite loops.

Code: `CODEALONGS/m8_agentic_frameworks/05_agentic_workflow_patterns.py`

---

# M8.4.2 · Workflow Pattern Catalog

| Pattern | Use when |
|---|---|
| chaining | the steps are always known |
| routing | the first branch depends on the request |
| parallel gather | facts can be collected independently |
| evaluator | generated work needs a check |
| handoff | another person, app, or agent must continue |

Pick the pattern before picking the framework.

---

# M8.4.3 · Least Autonomy That Works

```text
Fixed workflow > routed workflow > agent loop
```

Use the least autonomy that solves the measured problem.

- fixed workflow when the steps are known
- routed workflow when the first branch varies
- agent loop when the next step genuinely depends on observations

More autonomy means more tracing, limits, and evaluation.

---

# M8.4.4 · Pattern Applied

For the AAPL question:

```text
routing         choose the workflow
parallel gather price + allocation
RAG tool        search policy
calculator      check 36% against 35%
evaluator       verify note cites the limit
```

This is agentic because tools are assembled to answer.

It is controlled because Python owns the workflow.

---

# M8.4.5 · Workflow Step Costs

```text
one agent step =
  model tokens
  + tool latency
  + parsing risk
  + retry risk
  + trace volume
```

Frameworks make steps easier to build.

They do not make steps free.

Count steps before you ship the loop.

---

<!-- _class: lead -->

# M8.5 · End-To-End Agentic Application

End-to-end shape:

```text
question
  -> route
  -> gather tool facts
  -> search policy with LlamaIndex RAG
  -> check guideline
  -> draft answer
  -> trace result
```

Code: `CODEALONGS/m8_agentic_frameworks/06_end_to_end_agentic_app.py`

---

# M8.5.2 · Final Answer

The app should answer:

```text
Not allowed. 36% is above the 35% single-asset limit.
```

And it should retain evidence:

- AAPL price
- Alice's current AAPL allocation
- policy limit
- guideline result

Good agentic apps are inspectable.

---

# M8.5.3 · Handoff To M9

M8 builds a working agentic application.

M9 makes it product-safe:

- memory
- verification
- approval gates
- recovery from failed steps
- audit-friendly traces

This is the handoff to M9.
