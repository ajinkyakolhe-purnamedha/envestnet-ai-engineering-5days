---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M7.0.1 · The Agent Loop, By Hand

Building agents as plain Python control flow

By the end of this module you can:

- Explain the ReAct loop without framework language
- Turn model text into structured tool requests
- Validate and execute tool calls with Python
- Trace an agent run from question to final answer

<!--
This module builds one idea in layers: an agent is a bounded Python loop around
a model planner.

The model proposes the next step. Python validates, executes, records what
happened, and decides whether the loop continues. This boundary is the core AI
engineering idea in the module.
-->

---

<!-- _class: lead -->

# M7.1.1 · Chatbot vs. Task Loop

| Capability | Chatbot | Agent loop |
|---|---|---|
| Unit of work | One response | Multiple controlled turns |
| Outside facts | Must be pasted in | Can request tools |
| State | Conversation text | Text plus observations |
| Execution | Generates words | Python executes functions |
| Audit trail | Prompt and answer | Tool calls, results, errors |

```text
Chatbot:
User question -> LLM response -> text answer

Agent loop:
User question -> plan -> tool -> observation -> plan -> final answer
```

A chatbot answers from the context already available.

An agent loop can gather missing facts before answering.

<!--
The difference is control flow.

A chatbot turn can be enough when all facts are already in the prompt. An
agent loop is useful when the answer depends on facts the application must look
up or checks Python must perform.
-->

---

# M7.1.2 · Where The Intelligence Enters

The intelligent part is the **planner**.

Today, the planner starts as a normal Python function:

```python
def planner(state):
    if not state["observations"]:
        return {"tool": "get_current_price", "args": {"symbol": "AAPL"}}
    return {"final": "Write the advisor note from observations."}
```

Later, the planner becomes a model call that returns the same shape.

Python keeps the loop, tools, validation, and logs.

<!--
The model is injected at the planning point.

The runtime does not disappear when the planner becomes intelligent. The model
only replaces the decision rule that chooses "answer now" or "ask for this
tool next." Python still owns execution and safety.
-->

---

# M7.1.3 · Why Chat Is Not Enough

Advisor question:

> "Can Alice add more AAPL under the guideline?"

Missing facts:

- current simulated AAPL price
- Alice's current portfolio allocation
- guideline threshold
- whether the proposed allocation crosses the threshold

The task is not just language. It is a sequence of lookups and checks.

<!--
This is the product motivation for an agent.

The model should not invent the price, allocation, or guideline result. The
application should provide tools that retrieve or calculate those facts.
-->

---

# M7.1.4 · Agent Loop Anatomy

```text
Perception  ->  Planning  ->  Tool Execution  ->  Observation
   ^                                                   |
   |___________________________________________________|
```

Perception: read the request and current transcript.

Planning: choose final answer or next tool call.

Tool execution: Python runs a local function.

Observation: append the result to the transcript.

<!--
This is the core loop. Each pass through the loop gives the planner more
context than it had before.

The model does not run code. Python runs code and turns the result into an
observation the model can read on the next turn.
-->

---

# M7.1.5 · Model Owns vs. Python Owns

| Responsibility | Model planner | Python runtime |
|---|---|---|
| Choose next information need | Yes | No |
| Suggest tool name and args | Yes | No |
| Validate arguments | No | Yes |
| Execute function | No | Yes |
| Catch exceptions | No | Yes |
| Stop runaway loop | No | Yes |
| Write telemetry | No | Yes |

The runtime owns execution.

<!--
This table is the safety boundary.

ReAct is the name for this repeated reason-act-observe pattern. The "Act" part
is a request for action. The runtime decides whether the action is valid and
executes the Python function.
-->

---

# M7.1.6 · Code: Concept To Python

```python
state = {
    "question": "Can Alice add more AAPL under the guideline?",
    "observations": [],
}

def planner(state):
    if not state["observations"]:
        return {"tool": "get_current_price", "args": {"symbol": "AAPL"}}
    return {"final": f"Checked facts: {state['observations']}"}

def get_current_price(symbol: str) -> dict:
    return {"symbol": symbol, "price": 108.0}

for _ in range(3):
    step = planner(state)
    print("PLAN:", step)

    if "final" in step:
        print("FINAL:", step["final"])
        break

    # Actual tool execution happens here.
    result = get_current_price(**step["args"])
    observation = {"tool": step["tool"], "result": result}
    state["observations"].append(observation)
    print("OBSERVE:", observation)
```

```text
state = perception + observations
planner(state) = planning
get_current_price(...) = tool execution
state["observations"].append(...) = feedback
```

<!--
This is the smallest complete loop: state, planner, tool, observation, repeat,
final answer.

The planner is deterministic here so the control flow is visible. Later slides
replace the planner with model-produced structured text.
-->

---

# M7.1.7 · Experiment: Change The Decision

Change the question:

```python
state["question"] = "Can Alice add MSFT?"
```

Change the planner:

```python
def choose_price_tool(state):
    symbol = "MSFT" if "MSFT" in state["question"] else "AAPL"
    return {"tool": "get_current_price", "args": {"symbol": symbol}}
```

Checkpoint:

```text
We have a bounded Python loop.
Next we make the planner produce structured tool requests.
```

<!--
The experiment is deliberately small.

The goal is to see that the planner chooses a next step and the loop executes
that step through Python. The logic can be hardcoded before it becomes model
driven.
-->

---

<!-- _class: lead -->

# M7.2.1 · Function Calling Is Structured Text

The model still predicts tokens.

For tool use, we ask it to produce a stricter shape:

```json
{"tool": "get_current_price", "args": {"symbol": "AAPL"}}
```

The model is not calling Python.

It is proposing a next step as structured text.

```text
Model requests. Python executes.
```

<!--
Function calling becomes simpler when treated as structured output.

The client runtime interprets this structure. It should parse, validate, and
authorize the request before any function runs. The actual function call is
ordinary Python code.
-->

---

# M7.2.2 · Plain Answer vs. Tool Request

Plain text:

```text
Alice may need to check the portfolio allocation first.
```

Tool request:

```json
{"tool": "get_portfolio_allocation", "args": {"client_id": 1}}
```

Plain text can inform a human.

A tool request can drive a validated Python action.

The model writes the request. Python performs the action.

<!--
Structured output creates a bridge from language to software.

The bridge is only useful if the output has a predictable shape and the runtime
rejects bad shapes.
-->

---

# M7.2.3 · Why Schema Matters

Bad shape:

```json
{"tool": "price", "args": {"ticker": "apple"}}
```

Expected shape:

```json
{"tool": "get_current_price", "args": {"symbol": "AAPL"}}
```

Without a schema, models invent names, fields, and formats.

With a schema, Python can reject invalid requests.

<!--
Schemas are not only for documentation. They are executable validation.

This matters because model output is external input. Treat it with the same
skepticism as a request body from an API client.
-->

---

# M7.2.4 · Pydantic As Tool Contract

```python
from pydantic import BaseModel, Field

class CurrentPriceArgs(BaseModel):
    symbol: str = Field(description="Ticker symbol, for example AAPL")

valid = CurrentPriceArgs.model_validate({"symbol": "AAPL"})
print(valid.model_dump())

try:
    CurrentPriceArgs.model_validate({"ticker": "AAPL"})
except Exception as error:
    print(type(error).__name__)
```

Pydantic turns untrusted model arguments into typed Python data.

<!--
This is the first typed tool boundary.

The same class gives two things: validation at runtime and a schema that can be
shown to the model as the expected argument shape.
-->

---

# M7.2.5 · Tool Registry Shape

```python
def get_current_price(symbol: str) -> dict:
    return {"symbol": symbol, "price": 108.0}

def get_portfolio_allocation(client_id: int) -> dict:
    return {"client_id": client_id, "AAPL": 32.0, "cash": 18.0}

def check_guidelines(symbol: str, proposed_allocation_pct: float) -> dict:
    return {"symbol": symbol, "allowed": proposed_allocation_pct <= 35.0}

class PortfolioAllocationArgs(BaseModel):
    client_id: int

class GuidelineCheckArgs(BaseModel):
    symbol: str
    proposed_allocation_pct: float

TOOL_FUNCTIONS = {
    "get_current_price": get_current_price,
    "get_portfolio_allocation": get_portfolio_allocation,
    "check_guidelines": check_guidelines,
}

TOOL_SCHEMAS = {
    "get_current_price": CurrentPriceArgs,
    "get_portfolio_allocation": PortfolioAllocationArgs,
    "check_guidelines": GuidelineCheckArgs,
}
```

The registry is the list of operations the model may request.

<!--
The registry is also a permission boundary.

If a function is not in the registry, the model cannot call it through this
runtime. Adding a function to the registry should be a deliberate design
choice.
-->

---

# M7.2.6 · Code: Local Model Helper

```python
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_path = Path("OFFLINE-AI-Models/smollm2-135m-instruct")
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True).eval()

def ask_local_model(prompt: str, max_new_tokens: int = 60) -> str:
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    return tokenizer.decode(output[0, inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
```

Keep model loading in one helper so later recipes stay small.

<!--
This uses the local SmolLM2 bundle.

If running from inside `SLIDES-markdown`, change the path to
`../OFFLINE-AI-Models/smollm2-135m-instruct`. The helper returns raw generated
text, which is still untrusted input.
-->

---

# M7.2.7 · Code: Ask SmolLM2 For JSON

```python
prompt = """
Return JSON only.
Question: Can Alice add more AAPL?
Next tool call: {"tool":"get_current_price","args":{"symbol":"AAPL"}}
"""

raw_step = ask_local_model(prompt)
print(raw_step)
```

Offline model output is still untrusted input.

<!--
If the small local model emits extra text or imperfect JSON, that is expected
and useful for this lesson. The runtime must parse and validate before
execution.
-->

---

# M7.2.8 · Experiment: Invalid Output

Try these planner outputs:

```python
raw_outputs = [
    '{"tool":"get_current_price","args":{"symbol":"AAPL"}}',
    '{"tool":"get_current_price","args":{"ticker":"AAPL"}}',
    "Use the AAPL price tool.",
]
```

Ask:

```text
Which one can Python safely execute?
Which ones should become error observations?
```

Next: build the runtime that handles all three.

<!--
Invalid model output should not surprise the runtime.

The runtime's job is to parse valid requests, reject invalid requests, and
return useful observations about failures.
-->

---

# M7.2.9 · Code: JSON Request To Tool Observation

```python
import json

def get_current_price(symbol: str) -> dict:
    prices = {"AAPL": 108.0, "MSFT": 196.0}
    return {"symbol": symbol, "price": prices[symbol]}

raw_step = '{"tool":"get_current_price","args":{"symbol":"AAPL"}}'
print("MODEL OUTPUT:", raw_step)

step = json.loads(raw_step)
args = CurrentPriceArgs.model_validate(step["args"])
print("VALIDATED:", step["tool"], args.model_dump())

# Actual tool execution happens here.
result = get_current_price(**args.model_dump())
observation = {"tool": step["tool"], "result": result}

print("OBSERVATION:", observation)
```

The model requests the tool. Python executes the function.

```text
JSON output -> Pydantic args -> Python call -> observation
```

<!--
This slide connects the Section 2 concepts before the runtime details in
Section 3.

This is the self-contained Section 2 culmination. The model side may be
`ask_local_model(prompt)` or a deterministic raw string. The execution side is
the same either way: parse JSON, validate args, call Python, create observation.
-->

---

<!-- _class: lead -->

# M7.3.1 · Runtime Responsibilities

The runtime turns a model proposal into controlled execution.

It must:

1. parse model output
2. reject unknown tools
3. validate arguments
4. dispatch to Python
5. format observation
6. stop at `max_turns`

Frameworks package this flow. Building it once by hand removes the black box.

<!--
The runtime is deterministic even when the planner is probabilistic.

This is where ordinary engineering concerns return: parsing, validation,
function dispatch, exceptions, state updates, and loop limits.
-->

---

# M7.3.2 · Parse, Validate, Dispatch

```python
import json

def execute_tool(raw_text: str) -> dict:
    step = json.loads(raw_text)
    name = step["tool"]

    if name not in TOOL_FUNCTIONS:
        raise ValueError(f"Unknown tool: {name}")

    schema = TOOL_SCHEMAS[name]
    args = schema.model_validate(step["args"])
    # Generic dispatch: Python calls the selected tool here.
    return TOOL_FUNCTIONS[name](**args.model_dump())

raw = '{"tool":"get_current_price","args":{"symbol":"AAPL"}}'
print(execute_tool(raw))
```

This is the smallest safe execution boundary.

<!--
This one function combines the runtime stages:
parse text, check the tool registry, validate args, call the Python function.

In larger code, these steps may be split. Here they stay together so the
runtime boundary is visible in one place.
-->

---

# M7.3.3 · Code: Run The Loop

```python
def format_observation(tool: str, result: dict) -> dict:
    return {"role": "tool", "content": f"{tool} observation: {result}"}

def planner(messages: list[dict]) -> str:
    text = " ".join(message["content"] for message in messages)
    if "get_current_price observation" not in text:
        return '{"tool":"get_current_price","args":{"symbol":"AAPL"}}'
    return '{"final":"AAPL price was checked."}'

messages = [{"role": "user", "content": "Can Alice add AAPL?"}]

for turn in range(5):
    step = json.loads(planner(messages))
    if "final" in step:
        print(step["final"])
        break
    result = execute_tool(json.dumps(step))
    messages.append(format_observation(step["tool"], result))
```

The hard turn limit is a safety feature.

<!--
This loop is intentionally small.

It shows the core control flow: planner output, final check, tool execution,
observation append, repeat. Observation text should be concise, factual, and
specific because it is what the planner sees on the next turn.
-->

---

# M7.3.4 · Code: Runtime Loop With Model Planner

```python
messages = [{"role": "user", "content": "Can Alice add AAPL?"}]

for turn in range(5):
    raw_step = model_planner(messages)     # model plans from perception
    outcome = safe_execute(raw_step)       # Python parses, validates, executes

    if outcome["ok"]:
        step = json.loads(raw_step)
        messages.append(format_observation(step["tool"], outcome["result"]))
    else:
        messages.append({"role": "tool", "content": f"ERROR: {outcome}"})

    if "check_guidelines observation" in messages[-1]["content"]:
        print("Ready to draft advisor note.")
        break
```

This is the concept loop with the model actually choosing the next step.

<!--
This slide maps the text concepts to code directly:
messages are perception, `model_planner` is planning, `safe_execute` is the
runtime, and appending to messages is feedback for the next turn.

This recipe assumes `model_planner`, `safe_execute`, and `format_observation`
from the previous slides.
-->

---

# M7.3.5 · Code: Error Observation

```python
def safe_execute(raw_text: str) -> dict:
    try:
        return {"ok": True, "result": execute_tool(raw_text)}
    except Exception as error:
        return {
            "ok": False,
            "error_type": type(error).__name__,
            "message": str(error),
        }

bad = '{"tool":"get_current_price","args":{"ticker":"AAPL"}}'
print(safe_execute(bad))
```

Useful error observations help the planner correct the next step.

<!--
Do not hide runtime errors behind "something went wrong".

The loop can recover only if the next planner turn receives a clear observation
about the failure.
-->

---

# M7.3.6 · Code: Complete Advisor Loop

```python
def advisor_planner(messages):
    text = " ".join(m["content"] for m in messages)
    if "get_current_price observation" not in text:
        return '{"tool":"get_current_price","args":{"symbol":"AAPL"}}'
    if "get_portfolio_allocation observation" not in text:
        return '{"tool":"get_portfolio_allocation","args":{"client_id":1}}'
    if "check_guidelines observation" not in text:
        return '{"tool":"check_guidelines","args":{"symbol":"AAPL","proposed_allocation_pct":36}}'
    return '{"final":"Alice should not raise AAPL to 36%; the guideline limit is 35%."}'

messages = [{"role": "user", "content": "Can Alice add more AAPL?"}]

for turn in range(5):
    raw_step = advisor_planner(messages)
    step = json.loads(raw_step)
    if "final" in step:
        print("FINAL:", step["final"])
        break
    result = execute_tool(raw_step)
    messages.append(format_observation(step["tool"], result))
    print("OBSERVE:", messages[-1]["content"])
```

Now the runtime converges from question to checked facts to final note.

<!--
This slide makes the Chronos path concrete.

This is the Section 3 culmination: controller loop, planner, registry dispatch,
typed validation through `execute_tool`, observation append, and bounded stop.
The assistant researches and drafts; it does not execute investor trades.
-->

---

# M7.3.7 · Hand-Rolled Loop vs. Framework Loop

| Concern | Hand-rolled loop | Framework loop |
|---|---|---|
| Control flow | You write the `for turn in range(max_turns)` loop | Library owns the loop |
| Tool boundary | You parse, validate, dispatch | Library wraps tool registration |
| State | You append observations to `messages` | Library manages memory/state |
| Errors | You design error observations | Library provides callbacks/policies |
| Telemetry | You decide every trace field | Library emits built-in traces/hooks |

Use frameworks after you understand the primitive loop they package.

```text
Framework agent = planner + tools + runtime + state + trace, packaged together
```

<!--
This slide is the bridge from hand-built agents to framework agents.

The goal is not to argue against frameworks. The goal is to make frameworks
legible. LangChain, LlamaIndex, CrewAI, semantic-kernel-style runtimes, and
provider agent SDKs package the same responsibilities shown in this section:
planner call, tool registry, schema validation, execution, observation, loop
limits, and trace hooks.

For participant notes: if a framework agent feels confusing, inspect where it
stores messages, how it registers tools, how it validates tool arguments, what
happens on tool exceptions, and where it exposes the trace. Those are the same
questions answered by the hand-rolled loop.
-->

---

# M7.3.8 · Experiment: Force Failure And Fix It

Start with:

```python
bad = '{"tool":"get_current_price","args":{"ticker":"AAPL"}}'
print(safe_execute(bad))
```

Fix to:

```python
fixed = '{"tool":"get_current_price","args":{"symbol":"AAPL"}}'
print(safe_execute(fixed))
```

Checkpoint:

```text
We can now parse, validate, dispatch, observe, fail safely, and continue.
```

<!--
This is the hands-on runtime checkpoint.

The important lesson is not just that validation catches an error. The
important lesson is that Python controls what happens after the model produces
invalid output.
-->

---

<!-- _class: lead -->

# M7.4.1 · Why Agent Failures Need Traces

In a normal function call, a stack trace may be enough.

In an agent loop, failure may involve:

- model output
- parsing
- tool choice
- argument validation
- tool execution
- repeated retries
- max-turn stop

You need a trace of the loop, not just the final answer.

<!--
Agent failures are distributed across turns.

The final answer does not show which facts were checked, which tool failed, or
whether the loop stopped because it was done or because it hit a limit.
-->

---

# M7.4.2 · What To Log

Minimum trace fields:

```text
turn
raw_model_output
tool
raw_args
validated_args
result
exception
elapsed_ms
stop_reason
```

Good telemetry explains both success and failure.

<!--
The destination can be simple at first: a list of dictionaries, JSONL, or a
SQLite table.

The important part is the event shape. If the trace is readable, debugging and
review become possible.
-->

---

# M7.4.3 · Code: Trace Tool Execution

```python
from time import perf_counter

trace = []

def execute_with_trace(turn: int, raw_text: str) -> dict:
    started = perf_counter()
    record = {"turn": turn, "raw_model_output": raw_text}
    try:
        step = json.loads(raw_text)
        record["tool"] = step.get("tool")
        record["raw_args"] = step.get("args")
        args = TOOL_SCHEMAS[step["tool"]].model_validate(step["args"])
        record["validated_args"] = args.model_dump()
        # Traced dispatch: Python calls the selected tool here.
        result = TOOL_FUNCTIONS[step["tool"]](**args.model_dump())
        record["result"] = result
        return result
    except Exception as error:
        record["exception"] = type(error).__name__
        record["message"] = str(error)
        raise
    finally:
        record["elapsed_ms"] = round((perf_counter() - started) * 1000, 2)
        trace.append(record)
```

The wrapper records the run even when the tool fails.

<!--
This is the same execution boundary as before with telemetry added.

The trace records the raw model output before validation changes anything. That
helps explain whether the failure came from model output or tool execution.
-->

---

# M7.4.4 · Code: Success And Failure Trace

```python
good = '{"tool":"get_current_price","args":{"symbol":"AAPL"}}'
bad = '{"tool":"get_current_price","args":{"ticker":"AAPL"}}'

for turn, raw_step in enumerate([good, bad]):
    try:
        print("RESULT:", execute_with_trace(turn, raw_step))
    except Exception:
        print("ERROR RECORDED")

for record in trace:
    print(json.dumps(record))
```

The trace shows both the successful tool call and the rejected bad request.

```text
tool=get_current_price args={"symbol":"AAPL"} result=...
tool=get_current_price args={"ticker":"AAPL"} exception=ValidationError
```

<!--
The trace is evidence for both success and failure.

In an advisor workflow, the final paragraph is not enough. The checked facts,
raw arguments, validated arguments, exceptions, and elapsed time should be
visible.
-->

---

# M7.4.5 · Chronos Advisor Assistant Trace

```text
Question:
Can Alice add more AAPL under the guideline?

Trace:
1. get_current_price(AAPL)
2. get_portfolio_allocation(client_id=1)
3. check_guidelines(AAPL, proposed_allocation_pct=36)

Final note:
Do not raise AAPL to 36%; the guideline limit is 35%.
```

The agent researches and drafts. It does not execute trades.

<!--
This is the product integration point.

The Advisor Dashboard can use this loop as a research assistant. Trading
execution is intentionally outside the tool list because it requires approval,
authorization, and additional controls.

For failures, the same trace should capture the exception type and message. A
validation failure such as `{"ticker": "AAPL"}` instead of `{"symbol": "AAPL"}`
should be visible in the trace.
-->

---

<!-- _class: lead -->

# M7.L1 · Lab Objective

Build a simple ReAct agent loop in pure Python.

Open:

```text
CODEALONGS/code_alongs/07b_m7_manual_agent_loop.ipynb
```

Run from the `CODEALONGS/` folder:

```bash
uv sync --extra courseware
uv run jupyter lab
```

Question:

> "Can Alice add more AAPL under the guidelines? Show the facts you checked."

Tools:

```text
get_current_price(symbol)
get_portfolio_allocation(client_id)
check_guidelines(symbol, proposed_allocation_pct)
```

Use deterministic planning first. Swap in local SmolLM2 only after the loop works.

<!--
The lab builds the same architecture from this module. The notebook path is
shown on the slide so participants can start without guessing which file to
open.

The required path is deterministic so every participant can complete it. The
local model planner is a stretch once the runtime boundary is working.
-->

---

# M7.L2 · Lab Architecture

```text
messages
   |
   v
planner(messages)
   |
   v
tool step or final answer
   |
   v
execute_with_trace(step)
   |
   v
observation appended to messages
   |
   +-- repeat until final or max_turns
```

Deliverable: final advisor note plus printed trace.

<!--
This diagram is the complete system assembled in the lab.

Every piece has already appeared in the lecture: messages, planner, tool step,
runtime execution, observation, repeat, and trace.
-->

---

# M7.L3 · Lab Starter: Tools

```python
from pydantic import BaseModel

class CurrentPriceArgs(BaseModel):
    symbol: str

class PortfolioAllocationArgs(BaseModel):
    client_id: int

class GuidelineCheckArgs(BaseModel):
    symbol: str
    proposed_allocation_pct: float

def get_current_price(symbol: str) -> dict:
    return {"symbol": symbol, "price": 108.0}

def get_portfolio_allocation(client_id: int) -> dict:
    return {"client_id": client_id, "AAPL": 32.0, "cash": 18.0}

def check_guidelines(symbol: str, proposed_allocation_pct: float) -> dict:
    return {"symbol": symbol, "allowed": proposed_allocation_pct <= 35.0}
```

This cell defines the typed tool boundary.

<!--
The tools are deterministic so the lab can focus on the agent loop.

Later, these functions can be connected to Chronos database queries and
portfolio calculations.
-->

---

# M7.L4 · Lab Starter: Runtime

```python
from time import perf_counter

TOOL_SCHEMAS = {
    "get_current_price": CurrentPriceArgs,
    "get_portfolio_allocation": PortfolioAllocationArgs,
    "check_guidelines": GuidelineCheckArgs,
}
TOOL_FUNCTIONS = {
    "get_current_price": get_current_price,
    "get_portfolio_allocation": get_portfolio_allocation,
    "check_guidelines": check_guidelines,
}
trace = []

def execute_with_trace(turn: int, step: dict) -> dict:
    started = perf_counter()
    record = {"turn": turn, "tool": step["tool"], "args": step["args"]}
    args = TOOL_SCHEMAS[step["tool"]].model_validate(step["args"])
    # Lab dispatch: Python calls the selected tool here.
    result = TOOL_FUNCTIONS[step["tool"]](**args.model_dump())
    record["result"] = result
    record["elapsed_ms"] = round((perf_counter() - started) * 1000, 2)
    trace.append(record)
    return result
```

This cell defines what the runtime can execute and what it records.

<!--
This starter runtime is intentionally compact.

Participants can add exception logging after the basic loop works. The core
shape is registry, validation, dispatch, trace, return.
-->

---

# M7.L5 · Lab Starter: Planner And Loop

```python
def format_observation(tool: str, result: dict) -> dict:
    return {"role": "tool", "content": f"{tool} observation: {result}"}

def debug_planner(messages: list[dict]) -> dict:
    text = " ".join(message["content"] for message in messages)
    if "get_current_price observation" not in text:
        return {"tool": "get_current_price", "args": {"symbol": "AAPL"}}
    if "get_portfolio_allocation observation" not in text:
        return {"tool": "get_portfolio_allocation", "args": {"client_id": 1}}
    if "check_guidelines observation" not in text:
        return {"tool": "check_guidelines", "args": {"symbol": "AAPL", "proposed_allocation_pct": 36.0}}
    return {"final": "Alice should not raise AAPL to 36%; the guideline limit is 35%."}

messages = [{"role": "user", "content": "Can Alice add more AAPL under guidelines?"}]
for turn in range(5):
    step = debug_planner(messages)
    if "final" in step:
        print(step["final"])
        break
    result = execute_with_trace(turn, step)
    messages.append(format_observation(step["tool"], result))

print(trace)
```

This cell runs the complete deterministic debug loop.

<!--
This is the final assembly step.

The debug planner is deterministic. Replacing it with model output should not
change the runtime boundary: parse, validate, dispatch, observe, trace.
-->

---

# M7.L6 · Success Criteria

Success:

- loop stops with a final advisor note
- all three tools are called
- invalid arguments are rejected
- trace prints each tool call and result
- max turns prevents runaway execution

```text
model proposes, Python controls
```

<!--
These are the required checks for the lab.

The final answer is only one output. The trace is equally important because it
shows the facts the agent checked.
-->

---

# M7.L7 · Stretch Options

Stretch:

- replace deterministic `planner` with local SmolLM2 planner
- add exception details to `execute_with_trace`
- save trace as JSONL
- connect `get_current_price` to Chronos simulated-date prices
- connect `get_portfolio_allocation` to Chronos portfolio snapshot

Only take a stretch after the deterministic loop works.

```python
def llm_planner(messages: list[dict]) -> dict:
    raw_step = model_planner(messages)
    return json.loads(raw_step)
```

Then replace:

```python
step = debug_planner(messages)
```

with:

```python
step = llm_planner(messages)
```

<!--
Stretch work should preserve the same runtime boundary.

The model planner is a drop-in replacement for deterministic `planner`, not a
replacement for validation, dispatch, observations, loop limits, or telemetry.
-->
