---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M7 · Agentic LLMs

The model decides which capability is needed.

Python executes it.

By the end of this module you can:

- explain regular LLM vs agentic LLM
- expose Python functions as tools
- parse a model tool request
- run a small ReAct loop by hand
- read framework agents as packaged loops

---

<!-- _class: lead -->

# M7.1 · Why Agentic LLMs Exist

RAG assembles from retrieved paragraphs.

An agentic LLM assembles from function replies.

```text
RAG:
question -> search documents -> prompt with paragraphs -> answer

Agentic:
question -> choose function -> Python runs it -> observe result -> answer
```

RAG is for grounding in text.

Agents are for taking controlled steps through software.

Code: `CODEALONGS/m7_agentic_applications/01_regular_vs_agentic_llm.py`

---

# M7.1.2 · Regular LLM vs RAG vs Agentic

Question:

> Can Alice raise AAPL to 36% of the portfolio?

The model should not invent:

- current AAPL price
- Alice's current allocation
- concentration limit
- final allowed/not-allowed decision

Those are application facts and calculations.

The agent pattern lets the model ask for them.

---

# M7.1.3 · The Boundary

| Piece | Owned by |
|---|---|
| decide next information need | model |
| suggest tool name and args | model |
| validate tool name | Python |
| execute function | Python |
| record observation | Python |
| stop runaway loop | Python |

The model proposes.

Python executes.

---

<!-- _class: lead -->

# M7.2 · Tools Are Software Capabilities

A tool starts as normal software:

```python
def get_current_price(symbol: str) -> dict:
    prices = {"AAPL": 108.0}
    return {"symbol": symbol, "price": prices[symbol]}
```

The function already has the important engineering parts:

- name
- inputs
- return shape
- failure modes
- ownership

Code: `CODEALONGS/m7_agentic_applications/02_functions_as_tools.py`

---

# M7.2.2 · Tool Registry

Agents need a controlled list of allowed capabilities.

```python
TOOL_FUNCTIONS = {
    "get_current_price": get_current_price,
    "get_portfolio_allocation": get_portfolio_allocation,
    "check_guideline": check_guideline,
}
```

This is software engineering, not prompt magic.

The model can choose only from the registry.

---

# M7.2.3 · Tool Schema

The model also needs a description:

```python
TOOL_SCHEMAS = {
    "check_guideline": {
        "description": "Check whether a proposed allocation exceeds the 35% limit.",
        "args": {
            "symbol": "ticker symbol",
            "proposed_allocation_pct": "proposed percent",
        },
    }
}
```

Good tool schemas reduce guessing.

Bad tool schemas produce bad calls.

---

<!-- _class: lead -->

# M7.3 · From Tool Request To Safe Execution

The model still predicts tokens.

For tool use, we ask for a stricter shape:

```json
{"tool": "get_current_price", "args": {"symbol": "AAPL"}}
```

That JSON is not execution.

It is a request for Python to execute something.

Code: `CODEALONGS/m7_agentic_applications/03_llm_tool_request.py`

---

# M7.3.2 · Parse Before Execute

The runtime must ask:

- is the output parseable?
- is the tool allowed?
- are required args present?
- are arg values safe?
- how should errors be recorded?

The answer to a bad tool request is an observation, not a crash.

---

# M7.3.3 · Schema Validation Before Dispatch

Tool arguments are model output.

Treat them like an external API request:

```text
raw text -> parse JSON -> check tool allowlist -> validate args -> execute
```

Validation catches ordinary failures:

- wrong field name
- missing required value
- wrong type
- unsafe value

The model proposes arguments.

Python decides whether they are acceptable.

---

# M7.3.4 · Runtime Responsibilities

The runtime is deterministic software around a probabilistic planner.

It owns:

- parse model output
- reject unknown tools
- validate arguments
- dispatch to Python
- format observations
- record errors
- stop at `max_turns`

Frameworks package this runtime.

M7 makes it visible first.

---

<!-- _class: lead -->

# M7.3.5 · Python Executes, LLM Observes

```python
tool_request = json.loads(model_text)
tool_name = tool_request["tool"]
args = tool_request["args"]

result = TOOL_FUNCTIONS[tool_name](**args)
observation = {"tool": tool_name, "args": args, "result": result}
```

Python runs the function.

The model sees the observation on the next turn.

Code: `CODEALONGS/m7_agentic_applications/04_python_dispatch.py`

---

# M7.3.6 · Observation Is The Feedback Channel

```python
{
    "tool": "check_guideline",
    "args": {"symbol": "AAPL", "proposed_allocation_pct": 36.0},
    "result": {"allowed": False, "limit_pct": 35.0}
}
```

The observation is what lets the next model call reason from facts.

Without observations, the model is only chatting.

---

# M7.3.7 · Error Observations

Bad tool requests should enter the trace as observations:

```python
{"error": "invalid_json", "raw": model_text}
{"error": "unknown_tool", "tool": "send_wire_transfer"}
{"error": "missing_arg", "arg": "symbol"}
```

The runtime does not pretend the step worked.

It records why the step failed and lets the loop decide what happens next.

---

# M7.4 · The Agent Loop

Failure becomes observation.

A failed step should still produce useful state.

```python
observation = {
    "ok": False,
    "error": "unknown_tool",
    "requested_tool": "send_wire_transfer",
}
```

Now the loop can choose:

- retry with a valid tool
- ask for missing information
- stop with a controlled failure

Errors are part of the agent protocol.

---

<!-- _class: lead -->

# M7.4.2 · ReAct And The Agent Loop

ReAct means:

```text
Reason -> Act -> Observe -> Reason -> Act -> Observe -> Final
```

In code:

```python
for turn in range(max_turns):
    step = planner(state)
    if "final" in step:
        break
    observation = dispatch(step)
    state["observations"].append(observation)
```

Code: `CODEALONGS/m7_agentic_applications/05_react_loop.py`

---

# M7.4.3 · Why max_turns Exists

Agents can loop.

They can call the wrong tool.

They can repeat a failed call.

They can keep asking for missing facts.

`max_turns` is not optional infrastructure.

It is the first safety boundary.

---

# M7.4.4 · Model Owns vs Python Owns

| Responsibility | Model | Python |
|---|---:|---:|
| choose next information need | yes | no |
| suggest tool and args | yes | no |
| validate args | no | yes |
| execute function | no | yes |
| catch exceptions | no | yes |
| write telemetry | no | yes |
| stop runaway loop | no | yes |

Agents are useful because the model can decide.

Agents are safe only when Python controls execution.

---

# M7.4.5 · Trace The Run

```text
turn 1 -> get_current_price(AAPL)
turn 2 -> get_portfolio_allocation(Alice, AAPL)
turn 3 -> check_guideline(AAPL, 36.0)
turn 4 -> final answer
```

Final answer:

```text
Not allowed. 36% is above the 35% single-asset limit.
```

Trace is how we debug agent behavior.

---

# M7.4.6 · Trace Tool Execution

Trace one tool step as a record:

```python
{
    "turn": 2,
    "raw_model_text": "...",
    "tool": "get_portfolio_allocation",
    "args": {"client": "Alice", "symbol": "AAPL"},
    "result": {"allocation_pct": 32.0},
    "elapsed_ms": 4,
}
```

The trace is the debugger for the agent loop.

---

# M7.4.7 · What To Log

For every agent run, keep:

- original question
- model-requested tool
- parsed args
- validation result
- tool observation
- final answer
- stop reason

If you cannot replay the trace, you cannot debug the agent.

---

<!-- _class: lead -->

# M7.5 · Handoff To Frameworks

Every framework packages the same pieces:

| M7 concept | smolagents | LlamaIndex |
|---|---|---|
| tools | `@tool` | `FunctionTool` |
| loop limit | `max_steps` | workflow/agent limit |
| planner | model in agent | LLM in agent |
| observations | step logs | tool outputs/callbacks |

Code: `CODEALONGS/m7_agentic_applications/06_framework_mapping.py`

---

# M7.5.2 · Handoff To M8

In M7, we wrote the runtime by hand.

In M8, we use frameworks:

- smolagents for small tool agents
- LlamaIndex for tool and RAG integration

Keep the same mental model:

```text
The model proposes.
Python executes.
The trace proves what happened.
```

---

# M7.5.3 · Lab Success Criteria

Your plain-Python agent should:

- call only registered tools
- reject an `unknown_tool`
- record error observations instead of crashing
- stop at `max_turns`
- return the 35% guideline answer
- print a readable trace
