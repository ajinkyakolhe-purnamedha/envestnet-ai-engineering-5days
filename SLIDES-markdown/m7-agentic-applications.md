---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M7 · Agentic Application Building

Building hand-rolled agent control loops and tool execution protocols

By the end of this module you can:

- Explain the mechanics of the ReAct (Reason + Act) loop without framework abstraction
- Define deterministic Python tools with Pydantic schema validation
- Implement a hand-rolled agent execution loop with error handling
- Enable LLM self-correction by feeding tool execution errors back to context
- Evaluate when to use a hand-rolled loop vs. an orchestration framework (LangGraph)

<!--
Set expectations: 45 minutes lecture, followed by building a hand-rolled trading agent.

Before adopting agent frameworks (LangGraph, CrewAI), engineers must understand the underlying primitive loop.

An agent is simply a while loop around an LLM API call: the model requests a tool execution, Python executes the tool function, and the result is appended back to the conversation history.
-->

---

# The ReAct Pattern (Reason → Act → Observe)

```text
               +----------------------------------+
               |                                  |
               v                                  |
  [ User Query ] ---> 1. Reason (LLM Call)        |
                           |                      |
                  Does output request tool?       |
                     /           \                |
                 (No)             (Yes)           |
                 /                   \            |
        [ Final Answer ]        2. Act (Execute)  |
                                       |          |
                                3. Observe -------+
                                 (Append Result)
```

The model does not run external code. **Python code runs the tool** and feeds outputs back into the context window.

<!--
Walk through the ReAct loop step-by-step:
1. Reason: LLM inspects user query and available tool definitions, deciding whether to call a function or answer.
2. Act: Python code parses the JSON function call, validates arguments, and executes the target Python function.
3. Observe: Python code converts function return value into a message and appends it to the transcript.
-->

---

# Tool Definition & Schema Validation

```python
# snippets/m7/tool_schema.py — snippet file not yet written
# (module is a stub; the snippet must be authored before
#  delivery, per the module's transclusion reference)
```

### Schema Principles

1. **Pydantic Validation**:
   - `BaseModel` defines expected function arguments and types.
   - Field `description` strings tell the model *how* to use the argument.
2. **JSON Schema Export**:
   - `model_json_schema()` generates OpenAI-compatible tool specifications automatically.
3. **Deterministic Core**:
   - Tool functions (`get_stock_price`) remain standard, testable Python functions.

<!--
Tool schemas act as API contracts for the language model.

Providing clear parameter descriptions reduces argument hallucination (e.g. passing a date string in MM-DD-YYYY instead of ISO format YYYY-MM-DD).
-->

---

# Hand-Rolled Agent Loop

```python
# snippets/m7/react_loop.py — snippet file not yet written
# (module is a stub; the snippet must be authored before
#  delivery, per the module's transclusion reference)
```

### Execution Mechanics

1. **Iteration Boundary**:
   - Bound loop iterations (e.g. `max_turns=5`) to prevent infinite execution loops.
2. **Branching**:
   - If `resp.tool_calls` is empty, return final text completion.
   - If present, iterate over requested function calls.
3. **Transcript State**:
   - Append tool execution results using `role: "tool"`.

<!--
Walk through the hand-rolled execution loop line-by-line.

Notice that state management is simply appending dict objects to the `messages` list. Frameworks like LangGraph wrap this exact mechanism in graph state channels.
-->

---

# Error Recovery & Self-Correction

### Silent Failure (Bad Pattern)

```python
# Hiding errors breaks the loop
try:
    result = execute_tool(name, args)
except Exception as e:
    result = "Error occurred" # Vague!
```

If the tool returns a generic error string, the model cannot adjust its parameters and will repeat the identical invalid call.

### Explanatory Feedback (Good Pattern)

```python
# Pass exact error back to model
except ValidationError as e:
    result = (
        f"Invalid args for {name}: {e}. "
        "Required format: YYYY-MM-DD."
    )
```

By appending explicit validation error messages to the history, the LLM reads the error on the next iteration and self-corrects its inputs.

<!--
Self-correction requires informative error messages.

When a tool fails due to invalid parameters (e.g., non-existent stock symbol or wrong date format), pass the exact exception text back to the transcript. The model routinely fixes its mistake on turn +1.
-->

---

# Hand-Rolled Loop vs. Frameworks

| Dimension | Hand-Rolled Loop | Orchestration Framework (LangGraph) |
|---|---|---|
| **Code Footprint** | ~30 lines of Python | Framework dependency + graph setup |
| **Debuggability** | Full control; standard breakpoints | Inspecting framework state graphs |
| **State Persistence** | In-memory list append | Built-in checkpointers (SQLite / Postgres) |
| **Multi-Agent Routing** | Manual `if/else` control | Graph edges and conditional transitions |
| **Human-in-the-loop** | Manual input pauses | Native interrupt points & state resume |

Rule: **Use a hand-rolled loop for single-agent tool execution; reach for LangGraph when multi-agent routing or state persistence is required.**

<!--
Compare hand-rolled loops against frameworks.

For simple tool-calling agents, a 30-line hand-rolled loop is easier to test and maintain.

When building enterprise applications requiring multi-agent handoffs, human approvals, or persistent session state, frameworks like LangGraph provide necessary infrastructure.
-->

---

<!-- _class: lead -->

# 🧪 Lab: Building a ReAct Trading Agent for Chronos Wealth (60 min)

1. Define Pydantic tool schemas for `get_portfolio_value`, `get_stock_price`, and `execute_trade`.
2. Implement a 30-line hand-rolled ReAct loop with a 5-iteration limit.
3. Test self-correction by passing an invalid symbol to `get_stock_price` and observing parameter recovery.
4. Verify trades are point-in-time compliant and modify portfolio balance in SQLite.

Done when: `uv run pytest tests/labs/test_lab7_agent.py` passes clean.

<!--
Introduce Lab 7.

Participants build a hand-rolled trading agent that uses Chronos Wealth tools to inspect portfolio state, fetch price data, and place validated trades offline.
-->
