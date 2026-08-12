---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M8.0.1 · Agentic Frameworks & The Standard Patterns

Yesterday you wrote the runtime. Today you decide how much to hand over.

By the end of this module you can:

- Run yesterday's agent in 15 lines of smolagents
- Grow a toy agent into a production-shaped workflow
- Recognize the six standard agentic patterns
- Place the major frameworks on one map — and choose with criteria

<!--
M7 built the agent loop by hand: planner, tool registry, validation,
dispatch, observation, max_turns, trace. M8 never abandons that mental
model — every framework concept in this module maps back onto a piece
already written by hand, and the question that runs through the whole day
is: how much of that runtime gets handed over, and to whom?

The module moves from simple to complex: first one concrete
framework moment (the same agent, 15 lines, live and offline), then one
workflow grown step by step through the standard agentic patterns, then
three more frameworks read with a single lens, and only then the
landscape map. Framework names are easier to evaluate after participants
have seen the underlying runtime.
-->

---

<!-- _class: lead -->

# M8.1.1 · What You Own After M7

| Responsibility | Who wrote it yesterday |
|---|---|
| Loop + `max_turns` | you |
| Tool registry + schemas | you |
| Parse, validate, dispatch | you |
| Error observations | you |
| Trace | you |

~60 lines. Complete. Understood.

So why would anyone import a framework? **Watch.**

<!--
The starting inventory. After M7 the agent runtime — about 60 lines — is
fully owned and fully understood: the loop with its max_turns bound, the
tool registry with schemas, the parse-validate-dispatch runtime, the
error observations that contain bad model output, and the trace that
replays any run. Every row of this table is a slide from M7. The loop
works, so the practical question is why a framework is worth importing.

Hold the feature list until after the example. The next slide answers
with code: the same agent, one import, and fewer lines to maintain.
-->

---

# M8.1.2 · The Same Agent In 15 Lines

```python
from smolagents import (ToolCallingAgent,
                        TransformersModel, tool)

@tool
def get_current_price(symbol: str) -> dict:
    """Latest close for one symbol."""
    return {"symbol": symbol, "close": 80.46}

agent = ToolCallingAgent(
    tools=[get_current_price, check_guidelines],
    model=TransformersModel(model_id=str(CHAT_MODEL)),
    max_steps=3,
)
print(agent.run("Can Alice raise AAPL to 36%?"))
```

The `@tool` docstring is the schema. `max_steps` is your `max_turns`.

Full running version: `CODE-ALONGS/m8/smolagents_agent.py`

<!--
Yesterday's agent, rebuilt in smolagents — Hugging Face's deliberately
small agent library, built for open local models, which is exactly this
workshop's constraint and why it is the framework the room builds in.

The mapping to M7 is one-to-one. The @tool decorator reads the docstring
and type hints and builds what M7 called TOOL_SCHEMAS. The tools list is
TOOL_FUNCTIONS. TransformersModel is ask_local_model, pointed at the
committed SmolLM2 weights — no key, no network. max_steps is the for-loop
bound. The runtime, validation, and trace printing all live inside
ToolCallingAgent. Sixty lines became fifteen because the other forty-five
moved behind a constructor — not because they stopped existing.

Recipe on the slide, full code in the file — that split holds for every
code slide today. The file adds what the recipe omits: smolagents
requires an Args: section in each tool docstring, real price lookups, and
max_new_tokens for the tiny model. The file is the thing to run.
-->

---

# M8.1.3 · Trace From The Run

Observed run (SmolLM2-135M, CPU, ~28s):

```text
Step 1: Error while parsing tool call from model output
Step 2: Error while parsing tool call from model output
Step 3: Error while parsing tool call from model output
Step 4: max_steps reached, forced final answer:
FINAL: "Alice can raise AAPL to 36% by ..."   <- WRONG
```

The runtime was perfect. The planner never called a tool.

**Planner quality gates agent quality.**

<!--
This is the module's most important slide. Read
the trace line by line: every bad model output became a contained error
observation — M7's safe_execute, working. max_steps stopped the loop —
M7's bound, working. The runtime did its job perfectly. Then the model,
never having successfully called a tool or checked a single fact, was
forced to answer anyway — and got it backwards: the guideline caps a
position at 35%, so raising AAPL to 36% is not allowed.

The diagnosis matters more than the failure. Nothing here is a framework
bug: a 135M-parameter model simply cannot emit a well-formed tool call —
it is used because the room runs offline, not because it is good. With a
frontier model this exact file works: same code, better planner. The
slide's rule follows directly: planner quality gates agent quality. A framework
packages the runtime; it cannot upgrade the model's judgment.

The next section builds a version that answers correctly on this same
tiny model by moving the decision out of the planner.
-->

---

# M8.1.4 · A Framework Is Your Loop, Packaged

```text
Framework agent =
    planner + tools + runtime + state + trace,
    packaged together            (M7.3.7, yesterday)
```

What changes: who owns each piece.

What never changes:

```text
The model proposes. The runtime controls.
```

<!--
The definition, arriving after the experience instead of before it. What
just ran was the M7 loop — planner, registry, validation, dispatch,
observation, bound, trace — packaged behind one constructor. That is all
a framework agent is. Frameworks differ mainly in WHERE they put the
control written by hand yesterday: how much is configuration, how much is
still code, how much is hidden and hard to reach.

Two things follow. First, the reading lens for the rest of the day — and
for any framework pitch that ever lands on a desk: where did my registry
go, where did my max_turns go, where did my trace go? Second, the
invariant no framework changes: the model proposes, the runtime controls.
Who wrote the runtime is negotiable; that it exists is not.
-->

---

# M8.1.5 · Experiment: Read Your Own Trace

```bash
cd CODE-ALONGS
uv sync --extra agents
uv run python -m m8.smolagents_agent
```

While it runs (~30s), answer in M7 vocabulary:

1. Who caught `Error while parsing tool call`?
2. What stopped the loop at step 4?
3. The answer is fluent and wrong — which piece failed?

```text
Checkpoint: a framework runs our agent, and we
know its planner is the bottleneck.
Next: take the verdict away from the planner.
```

<!--
First hands-on moment of the day: the trace
from M8.1.3, now on everyone's own machine. Watching a failure on a slide
and producing it yourself are different kinds of knowledge.

The three answers, in M7 vocabulary: (1) the parse errors were caught by
the runtime's safe_execute equivalent — every bad model output became a
contained error observation; (2) max_steps stopped the loop — the same
bound M7 called max_turns; (3) the piece that failed is the planner — the
runtime never failed at all. Anyone who can give those three answers owns
the trace, not just the slide.

The checkpoint closes the section: participants should be able to name
the runtime pieces in the trace. If `uv sync` is still running, continue;
the lab repeats this command as its first step.
-->

---

<!-- _class: lead -->

# M8.2.1 · The Pattern Catalog

Six standard shapes for agentic applications:

```text
chaining        A -> B -> C, fixed order
routing         classify, then branch
parallelization fan out, gather
evaluator       draft, critique, revise
orchestrator    one planner delegates to workers
handoff         agent passes control to agent
```

We will **grow one artifact** through the first four:

the advisor note workflow — the one M8.1.3 got wrong.

<!--
The pattern names follow the now-standard industry taxonomy (Anthropic's
"Building Effective Agents" popularized it). The six form a spectrum from
deterministic workflow to autonomous agent: in a chain, Python decides
everything; in a ReAct loop, the model decides everything. M7's loop sits
at the far autonomous end — which is exactly why it needed the most
safety machinery.

This section is not a tour of six disconnected examples. It takes the
question the autonomous agent answered WRONG a moment ago and builds the
workflow that answers it right — then upgrades that same workflow three
times: a front door (routing), a faster gather (parallelization), a
quality gate (evaluator). One artifact, growing. Orchestrator and handoff
close the section as read-along shapes for the situations the fixed
workflow cannot handle — when the work list itself varies per question.

Every build slide is a runnable offline file in CODE-ALONGS/m8/, so every
step of the artifact can be executed, not just read.
-->

---

**The Advisor Workflow · 1 of 4**

# M8.2.2 · Chaining: The Workflow That Gets It Right

```python
facts = {
    "price": get_current_price("AAPL"),
    "allocation": get_portfolio_allocation(1),
    "check": check_guidelines("AAPL", 36.0),
}                                     # step 1: gather

verdict = ("blocked by the 35% limit"
           if not facts["check"]["allowed"]
           else "within guidelines")  # step 2: decide

note = generate(                      # step 3: draft
    f"Facts: {facts}. Verdict: {verdict}. "
    "Write a 2-sentence advisor note.")
```

```text
gather  = tool execution, ordered by Python (M7: runtime)
decide  = planning -- owned by Python, not the model
draft   = the model's only job: language
```

Full running version: `CODE-ALONGS/m8/pattern_chaining.py`

<!--
M8.1.3's question is answered correctly by the same tiny model because
the model no longer owns the verdict. The key change is precise: M7's
loop let the planner choose every step; this chain hard-codes the steps
and uses the model only for prose. The verdict is computed by Python
BEFORE the model is involved, so the note
cannot get the answer wrong the way the autonomous agent did.

The mapping fence ties each step back to M7 anatomy: gather is tool
execution with Python ordering the calls, decide is planning owned by
Python instead of the model, draft is the model's only remaining job —
language.

The recipe is the feature; the file only adds imports and prints.
This shape is not a teaching simplification: a chain with the model
drafting prose at the end is the pattern most shipping "agent" products
actually are.
-->

---

**The Advisor Workflow · 2 of 4**

# M8.2.3 · Routing: A Front Door

```python
ROUTES = {
    "price":  ["What is AAPL trading at?", ...],
    "policy": ["What does our policy say?", ...],
    "trade":  ["Buy 100 shares of AAPL now.", ...],
}

def route(question: str) -> str:
    q = embed([question])[0]
    scores = {label: max(similarity(q, embed([ex])[0])
                         for ex in examples)
              for label, examples in ROUTES.items()}
    return max(scores, key=scores.get)
```

```text
route() = planning, decided by embeddings (M2 pattern)
branch  = Python control flow -- price/policy run the
          workflow; "trade" is refused, no tool touched
```

Full running version: `CODE-ALONGS/m8/pattern_routing.py`

<!--
The workflow gains a front door: only questions the router recognizes
ever reach the chain, and trade-like requests are refused by Python
before any tool is touched — the same governance rule as M7, where no
trade tool was ever registered in the first place. Refusing in code is
more reliable than asking the model to refuse.

The router uses M2's embedding pattern: SmolLM2 cannot classify reliably as a chat
model ("answer with one word" defeats it), but the BGE embeddings are
excellent — so the router embeds the question and compares it to a few
example phrasings per branch. Classification without a classifier.

Implementation note from building this slide: with only ONE example per route,
"How expensive is MSFT right now?" misrouted to policy. Two examples per
intent fixed every test case. The general rule: routes are DEFINED by
their examples, so each intent needs enough phrasings to cover how people
actually ask. The slide shows one example per route for space; the file
carries two or more.
-->

---

**The Advisor Workflow · 3 of 4**

# M8.2.4 · Parallelization: A Faster Gather

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as pool:
    price = pool.submit(get_current_price, "AAPL")
    alloc = pool.submit(get_portfolio_allocation, 1)
    check = pool.submit(check_guidelines, "AAPL", 36.0)

facts = {"price": price.result(),
         "allocation": alloc.result(),
         "check": check.result()}
```

```text
fan-out = tool execution, three at once
facts   = observations, gathered not appended
decide + draft = unchanged -- the workflow's steps 2-3
```

Full running version: `CODE-ALONGS/m8/pattern_parallel.py`

<!--
Step 1 of the chain, fanned out. The three lookups do not depend on each
other, so they run at once; steps 2 and 3 of the workflow do not change
at all. The mapping fence says it plainly: fan-out is still tool
execution, just three at a time, and the results are observations
gathered into one dict instead of appended one by one.

There is nothing unusual in the implementation here. It is ThreadPoolExecutor
— standard-library Python that predates this workshop. When a framework
advertises "parallel tool calls", this is what ships underneath. The
pattern earns its place when the lookups are genuinely independent and
slow (three API calls, not three dict reads).

A callback lands this afternoon: in the PydanticAI port, Gemini requests
all three tools in ONE model response, unprompted — the same pattern,
initiated by a frontier model on its own.
-->

---

**The Advisor Workflow · 4 of 4**

# M8.2.5 · Evaluator: A Gate On The Draft

```python
draft = generate("Write a 2-sentence advisor note "
                 f"from: {facts}")

problems = []
if "35" not in draft:
    problems.append("must cite the 35% limit")
if len(draft.split()) > 60:
    problems.append("too long")

if problems:
    draft = generate(f"Rewrite: {draft}. "
                     f"Fix: {problems}")
```

```text
draft    = model output = untrusted input (M7.2)
problems = validation, aimed at prose instead of JSON
rewrite  = one bounded retry -- max_turns for quality
```

Full running version: `CODE-ALONGS/m8/pattern_evaluator.py`

<!--
The workflow is complete: routed front door, parallel gather, Python
verdict, drafted note — and now the draft itself faces a critic before
anyone sees it. The key move in the mapping fence: model output is
UNTRUSTED INPUT, exactly as M7.2 established for JSON — the evaluator
just aims that same suspicion at prose. Here the critic is deterministic
Python: checkable rules (does the note cite the limit? is it under the
length cap?), not another model opinion. That ordering previews M13: the cheapest
quality gate is an assertion, and LLM-as-judge comes only after the rules
run out.

The single revision pass is deliberate. Evaluator loops need a bound
exactly like agent loops — one rewrite is max_turns for quality; without
it, a stubborn draft spins forever.

Four slides, one artifact: this is the workflow the lab assembles over
real Chronos data. M9 then connects it to the advisor dashboard.
-->

---

**Shapes You'll Meet · 1 of 2**

# M8.2.6 · Orchestrator–Workers

```python
def research_worker(symbol: str) -> dict:
    return {"symbol": symbol,
            "price": get_current_price(symbol),
            "alloc": get_portfolio_allocation(1)}

def orchestrator(question: str) -> str:
    symbols = [s for s in ["AAPL", "MSFT", "GLD"]
               if s in question]          # plan
    findings = [research_worker(s)
                for s in symbols]         # delegate
    return generate(                      # synthesize
        f"Findings: {findings}. Draft the "
        "advisor summary in 2 sentences.")
```

```text
plan       = planning (here a rule; at scale, a model)
delegate   = tool execution, one worker per fact
synthesize = observations -> final answer
```

Full running version: `CODE-ALONGS/m8/pattern_orchestrator.py`

<!--
Not part of the built workflow — this is the shape for the situation the
fixed chain cannot handle: when the WORK LIST itself varies per question.
"Tell me about AAPL" needs one worker; "compare my holdings" needs three;
a chain cannot know that in advance, an orchestrator decides it at
runtime.

The three-step anatomy — plan, delegate, synthesize — maps onto M7
vocabulary in the fence: planning produces a work list instead of a next
action, delegation is tool execution with one worker per fact, synthesis
turns observations into the final answer. In this offline version the
planning step is a deterministic rule (which symbols appear in the
question); in a frontier-model system that step is a model call returning
a work list. Same shape either way.

This is also the architecture of every "deep research" product currently
shipping: an orchestrator fans out searches, workers read independently,
a synthesizer writes one report.
-->

---

**Shapes You'll Meet · 2 of 2**

# M8.2.7 · Multi-Agent Handoff

```python
researcher = ToolCallingAgent(
    tools=[get_current_price], model=model,
    name="researcher",
    description="Gathers facts about holdings.")

manager = ToolCallingAgent(
    tools=[], model=model, max_steps=3,
    managed_agents=[researcher])

manager.run("Ask the researcher for the AAPL price.")
```

```text
managed agent = a tool with a planner inside
manager       = planning over planners
max_steps     = still the only thing stopping it
```

Full running version: `CODE-ALONGS/m8/pattern_handoff.py`

<!--
The core idea in one line of the fence: a managed agent is a tool with a
planner inside. smolagents' managed_agents is the cleanest expression —
a sub-agent is registered exactly like a tool, with a name and a
description the manager reads when deciding whom to call. The manager is
planning over planners, and max_steps is still the only thing stopping
any of it. The same idea wears different names everywhere: OpenAI's SDK
calls it "handoffs", CrewAI calls it a "crew", LangGraph draws it as
subgraphs. Specialists with narrow toolsets, composed by a coordinator.

Run on SmolLM2, this fails for the same reason M8.1.3 did — every
planner in the tree is still a 135M model — and that failure is itself
informative: multi-agent multiplies planner quality, in both directions.

The warning: multi-agent is the most oversold pattern in the
industry. Two agents that share all tools are strictly worse than one
agent — more cost, more latency, more failure surface, zero added
capability. Split only when the toolsets or instructions genuinely
differ.
-->

---

# M8.2.8 · Choosing: Least Autonomy That Works

```text
know the steps?           -> chaining
known branches?           -> routing
independent lookups?      -> parallelization
quality gate needed?      -> evaluator-optimizer
work list varies?         -> orchestrator-workers
steps genuinely unknown?  -> ReAct agent (M7)
```

The workflow we just built used the first four because its steps are known.

More autonomy adds reliability cost. Use it when the problem requires it.

<!--
The section closes with the module's core engineering judgment. The six
patterns are ordered by increasing autonomy, and the decision procedure
is: walk down the list and take the FIRST one that fits. The fully
autonomous loop is the last resort, not the default — reached only when
the steps genuinely cannot be known in advance.

The reasoning: every notch of autonomy transfers control from Python to
the model, and M8.1.3 showed what that costs — the more the model
controls, the more planner quality gates everything. The advisor report
has known steps, so this section built it as a workflow with the model
drafting prose, and that version IS more reliable than the autonomous
one on the same tiny model. The comparison between M8.1.3 and M8.2.2 is
the strongest evidence in the module.

The closing line should be read as an engineering constraint: autonomy
costs reliability, so spend it only when the problem demands it.
-->

---

# M8.2.9 · Experiment: Break The Router

```bash
uv run python -m m8.pattern_routing \
  "How much cash would selling AAPL raise?"
```

Observed: `price 0.823 · trade 0.773` — a sell walks in the front door.

1. Decide: price question, or trade intent?
2. Encode your decision — add one `trade` example, rerun
3. Hunt your own near-miss (best found so far: margin 0.001)

```text
Checkpoint: the workflow is ours -- and its front
door is exactly as good as its examples.
Next: the same agent, three more frameworks.
```

<!--
Verified run: the sell-shaped question scores price 0.823, trade 0.773 —
it routes to price and gets a helpful answer instead of a refusal.

Step 1 is a real product decision, not a trick question. "How much WOULD selling
raise" is arguably a valuation question, and a reasonable person can
defend answering it. The governance position is that anything sell-shaped
hits the refusal path — advisors do not execute trades — and whichever
way the decision goes, it should be a decision encoded as an
example, not an accident of similarity scores. The fix is one line:
adding "Sell my AAPL shares for cash." to the trade route lifts trade to
0.860 and wins (verified).

Step 3's benchmark: "Rebalance Alice out of AAPL into cash." routes to
trade by 0.716 vs 0.692 — correct, but a coin flip. The useful part is
the margin: routes are defined by examples, so the router's safety
margin is a NUMBER — printable, testable, regression-checkable. M13
builds that instinct into a test suite.
-->

---

<!-- _class: lead -->

# M8.3.1 · Same Agent, Three More Ways

You have seen one framework deeply. Now read three more:

> "Can Alice raise AAPL to 36% of her portfolio?"

Same three tools every time:

```text
get_current_price(symbol)
get_portfolio_allocation(client_id)
check_guidelines(symbol, proposed_allocation_pct)
```

Watch one thing: **where does the M7 runtime go?**

<!--
The section's method is controlled comparison: one slide per framework,
same question, same three tools, so the only thing that varies is the
framework's shape. Whatever differs between slides IS the framework.
Complexity rises deliberately: typed simplicity (PydanticAI), then
tools-plus-indexes (LlamaIndex), then explicit graphs (LangGraph).

These three need a real tool-calling model — a 135M planner cannot
exercise them, as M8.1.3 proved. They run on Gemini
(gemini-2.5-flash-lite, the cheapest tier; a full run costs a fraction
of a cent). In the room that means read-along on the instructor's key;
at a desk later, any personal key works. All files live in
CODE-ALONGS/m8/ and run with `uv run python -m m8.<name>` from the
CODE-ALONGS folder.

The one thing to track through all three slides is the question at the
bottom: where does the M7 runtime go?
-->

---

# M8.3.2 · PydanticAI — Your Contracts Are The API

```python
from pydantic_ai import Agent

class AdvisorNote(BaseModel):
    recommendation: str
    allowed: bool

agent = Agent(
    "google:gemini-2.5-flash-lite",
    tools=[get_current_price,
           get_portfolio_allocation,
           check_guidelines],
    output_type=AdvisorNote,
)
result = agent.run_sync(QUESTION)
print(result.output)   # a valid AdvisorNote
```

`output_type` guarantees a valid `AdvisorNote` — or the model is re-asked.

Full running version: `CODE-ALONGS/m8/pydanticai_agent.py`

<!--
PydanticAI's one idea: the contracts ARE the API. Plain functions with
type hints become tools — the M7 registry, derived automatically — and
the final answer is not free text but a validated Pydantic model,
declared with output_type. When the model returns something that fails
validation, PydanticAI re-prompts it automatically: the error-observation
retry built by hand in M7, shipped as a built-in. For anyone who
internalized M2's structured-output lesson and M7's runtime, this is the
framework with the smallest conceptual distance — the strongest first
recommendation for a next project that has an API key.

Verified run (gemini-2.5-flash-lite): a correct AdvisorNote with
allowed=False and a recommendation citing the 35% limit. The trace also
shows something worth noticing: all three tools requested in ONE model
response, executed as parallel tool calls — the M8.2.4 pattern, done by
a frontier model unprompted.

The file adds the pydantic import, a facts_checked field, a system
prompt, and the message-trace printout — and needs GEMINI_API_KEY in
CODE-ALONGS/.env.
-->

---

# M8.3.3 · LlamaIndex — Your Retriever Becomes A Tool

```python
from llama_index.core.agent.workflow import (
    FunctionAgent)
from llama_index.llms.google_genai import GoogleGenAI

def search_investment_policy(query: str) -> str:
    """Return policy paragraphs matching the query."""
    ...   # keyword match today; M4 vector index later

agent = FunctionAgent(
    tools=[search_investment_policy,
           check_guidelines],
    llm=GoogleGenAI(model="gemini-2.5-flash-lite"),
)

print(await agent.run("Is 36% in one stock allowed?"))
```

Day 2 RAG was a pipeline you ran. Now it is a tool the **agent** decides to use.

Full running version: `CODE-ALONGS/m8/llamaindex_rag_agent.py`

<!--
LlamaIndex's one distinctive idea: agents and RAG share a toolbox — and
that idea is the bridge between Day 2 and Day 3. In M4, retrieval was a
pipeline walked through once: query, chunks, answer, done. Here the same
retrieval is just another tool: FunctionAgent wraps the plain function
into a FunctionTool from its type hints and docstring, and the AGENT
decides when the question needs policy text — combinable with
check_guidelines in a single run. RAG stops being an architecture and
becomes a capability an agent can reach for.

The demo keeps retrieval as a keyword match so it runs anywhere; in
production the M4/M5 vector index drops in behind a QueryEngineTool and
the agent code does not change. That is the practical value of tools as
an abstraction.

API gotcha, in both files: the API is async-first, and agent.run must be
called inside a running event loop — wrap it in async main() +
asyncio.run(main()); a module-level call raises "no running event loop".

Verified runs (gemini-2.5-flash-lite): plain port — "Alice cannot raise
AAPL to 36% ... maximum of 35%"; RAG agent — "The policy states that no
single holding may exceed 35% of total portfolio value. Therefore, 36%
in one stock is not allowed."

Files: llamaindex_rag_agent.py (this slide) and llamaindex_agent.py (the
plain three-tool port, same shape as the other frameworks, kept for
completeness). The file fills in the elided retrieval body, adds a system
prompt, and wraps the await in async main().
-->

---

# M8.3.4 · LangGraph — The Loop As A Graph

```python
from langchain.agents import create_agent

agent = create_agent(
    ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite"),
    tools=[get_current_price,
           get_portfolio_allocation,
           check_guidelines],
)
state = agent.invoke(
    {"messages": [("user", QUESTION)]},
    config={"recursion_limit": 10},
)
print(state["messages"][-1].content)
```

```text
agent -> tools -> agent -> ... until no tool calls remain
```

Full running version: `CODE-ALONGS/m8/langgraph_agent.py`

<!--
LangGraph's idea: the loop drawn as an explicit graph. The vocabulary
maps directly onto M7 — "state" is the messages list, the edge that
cycles agent -> tools -> agent is the for-loop, recursion_limit is
max_turns. What ran here is create_agent, the prebuilt shortcut; the real
power, and the real learning curve, is defining custom nodes and edges —
approval steps, branches, parallel fan-outs as graph topology. That
explicit control is what makes LangGraph the industry default for complex
workflows, and equally what makes it overkill for a three-tool question
like this one.

A churn note that matters later in the deck: LangGraph v1 moved
create_agent into langchain.agents, and the older
langgraph.prebuilt.create_react_agent is deprecated — this slide had to
be rewritten between authoring and delivery because of it.

Verified run (gemini-2.5-flash-lite): correct refusal citing the 35%
limit, with the full message trace — one AIMessage carrying three tool
calls, three ToolMessages, one final AIMessage. The file adds the
langchain_google_genai import, a system prompt, and the trace printout.
-->

---

# M8.3.5 · Where Did Your Runtime Go?

| You wrote (M7) | smolagents | PydanticAI | LangGraph |
|---|---|---|---|
| tool registry | `tools=[...]` | `tools=[...]` | `tools=[...]` |
| schemas | docstrings | type hints | type hints |
| parse+validate | internal | internal + retry | ToolNode |
| `max_turns` | `max_steps` | usage limits | `recursion_limit` |
| trace | printed steps | `all_messages()` | `state["messages"]` |

~60 hand-written lines → ~20 lines of configuration.

**You can now read any of them.** That is the skill this section builds.

<!--
The section closes with one table. Every framework column answers the
same five questions — and the five answers were memorized before lunch,
because the left column is the code written by hand in M7. Reading the
table row by row: tool registries are identical everywhere; schemas come
from docstrings or type hints; parsing and validation are internal (with
PydanticAI adding automatic retry, LangGraph isolating it in a ToolNode);
every framework has a loop bound under a different name; every framework
keeps a trace under a different accessor.

The habit to keep: whenever a framework agent feels confusing — any
framework, including ones not on this slide — ask the M7.3.7 questions.
Where are messages stored, how are tools registered, how are arguments
validated, what happens on exceptions, where is the trace. Sixty
hand-written lines became twenty lines of configuration, and writing
those sixty lines is what makes the framework versions readable.
-->

---

# M8.3.6 · Experiment: Find Your Runtime In The Files

Open the three ports in `CODE-ALONGS/m8/`. In each file, point at the line that:

- bounds the loop — M7's `max_turns`
- registers the tools
- would contain `get_current_price("TSLA")` raising
- exposes the trace

No key needed to read. Run them at your desk later with yours.

```text
Checkpoint: you can open any framework's agent
file and point at every M7 component.
Next: the whole landscape, on one map.
```

<!--
A reading experiment, scoped to the room constraints: with no API keys in the room, the
cloud ports are read rather than run — and reading a framework file with
a checklist is precisely the skill this section promised. This is the
M8.3.5 table, rebuilt by hand against real files.

The third bullet is the sharp one, because the frameworks genuinely
differ. DRAFT — verify before each delivery: smolagents turns a tool
exception into an error observation and the loop continues; LangGraph's
ToolNode catches it and hands the model an error ToolMessage; PydanticAI
by default lets the exception propagate and crash unless the tool raises
ModelRetry. The safe_execute decision M7 made by hand is a decision each
framework makes differently — and one of them makes it the opposite way.
Knowing which, before production, is the difference between a contained
error and a 3am page.
-->

---

<!-- _class: lead -->

# M8.4.1 · The Landscape: Two Families

**Provider SDKs** — each cloud wants to own your agent loop:

OpenAI Agents SDK · Claude Agent SDK · Google ADK · AWS Bedrock

**Open source, model-agnostic** — you pick the model:

LangGraph · CrewAI · PydanticAI · LlamaIndex · smolagents

<!--
Now the map, after the territory: one framework run, three read, and this
section places all of them — plus the ones skipped — so the names in job
postings and vendor pitches have somewhere to land.

The two families divide on a single question: who chooses the model.
Provider SDKs (OpenAI, Anthropic, Google, AWS) are excellent inside their
own ecosystem and are how each vendor wants agents built — the trade is
polish for commitment. Open-source, model-agnostic frameworks let the
same agent point at any model, including a local one — which is why
everything that RAN today lives in the second family: the room's only
available planner is a local SmolLM2, and only model-agnostic frameworks
can reach it.
-->

---

# M8.4.2 · The Comparison Checklist

When a framework pitch reaches you, score it against
what real products need:

- **branch** — "if the guideline fails, research the policy instead"
- **retry** — tool timeouts, malformed model output, backoff
- **parallel** — check five holdings at once
- **pause** — wait for human approval, resume tomorrow
- **stream** — show progress, not a spinner
- **swap** — cheap model for routing, big model for drafting

Each is 30–100 lines if you write it yourself.

<!--
Six capabilities real agent products end up needing, usable two ways: as
a requirements list when building, and as a scoring rubric when a
framework pitch arrives. Each item is 30–100 lines to hand-write. Add
them all to the 60-line M7 loop and
the result is a 600-line private framework that nobody else can debug and
nobody documents. A framework is that same 600 lines, written once,
documented, and shared across the industry. The build-vs-buy question is
really "whose 600 lines?"

Today's code already demonstrated some rows: parallel (M8.2.4, and
Gemini requesting three tool calls in one response), retry (PydanticAI's
validation re-prompt). Pause and stream are M9's subject — human
approval gates and progressive output are what turn a workflow into a
product feature.
-->

---

# M8.4.3 · What A Step Costs

```text
one model call = framework system prompt
              + every tool schema
              + the FULL history so far
              + the newest observation
```

- Measured: smolagents injects **1,054 tokens** before your question — more than your whole M7 loop
- History is resent every step: turn N pays for turns 1 to N−1 again
- A managed sub-agent pays that bill per delegation

M2's meter never stopped running.

<!--
The bridge back to M2's token economics, now that "step" means something
concrete. The 1,054 is a real measurement: agent.system_prompt on the
smolagents ToolCallingAgent from this morning is 3,656 characters,
counted with M2's count_tokens — the framework spends more tokens
instructing the model than M7 spent implementing the entire runtime.
Nothing in the trace shows this; it is invisible until the bill arrives.
DRAFT — the number moves with smolagents versions; re-measure per
delivery with one line: count_tokens(agent.system_prompt).

The growth is the second surprise: because models are stateless, the full
history is resent on every step, so a ten-turn agent pays for turn one
ten times — cost grows roughly with the square of the conversation
length. And each of M8.2.7's managed agents carries its OWN system prompt
and its OWN history: multi-agent multiplies the bill, not just the
capability. This is why M8.4.2's "swap" criterion exists — route with a
cheap model, draft with a big one — and why M2 taught prompt caching:
providers cache the repeated prefix, and that caching is the only reason
long agent runs are affordable at all.
-->

---

# M8.4.4 · The Case Against Frameworks

- **Churn** — `create_react_agent` deprecated while this deck was written (M8.3.4)
- **Opacity** — debugging through layers you didn't write
- **Overhead** — 1,054 tokens per step, invisible until the bill
- **Lock-in** — prompts and state shaped like the vendor

A 60-line loop you fully understand is a valid production choice.

```text
Use the checklist (M8.4.2) --
not brand preference or perceived complexity.
```

<!--
The counterweight. After a day of arguing that frameworks are the same
loop packaged, name what the package costs. Churn:
this very deck's LangGraph slide had to be rewritten because the
canonical entry point deprecated between authoring and delivery — not a
LangGraph insult, just what a fast-moving abstraction layer feels like
from below, and agent frameworks are the fastest-moving layer in the
stack right now. Opacity: a bug five layers into someone else's
abstraction costs more to find than a bug in sixty lines you wrote.
Overhead: the previous slide's 1,054 tokens, spent on every single step.
Lock-in: prompts, state schemas, and orchestration written in a vendor's
shapes do not port out easily.

The conclusion is balanced, not anti-framework. The
moment a project needs pause, stream, and retry together, sixty owned
lines become the 600-line private framework nobody else can debug. Both
failure modes are common: adopting a framework too early, or refusing one
after the requirements justify it. The M8.4.2 checklist turns that into
a decision.
-->

---

# M8.4.5 · Provider SDKs

| SDK | Shape | Distinctive |
|---|---|---|
| OpenAI Agents SDK | `Agent` + `Runner` | handoffs, guardrails, sessions |
| Claude Agent SDK | agent harness | the engine behind Claude Code |
| Google ADK | code-first agents | workflow agents, eval tooling |
| AWS Bedrock AgentCore | managed runtime | enterprise deploy + IAM story |

All four assume a frontier tool-calling model on the other end.

<!--
DRAFT — facts that rot. This table was accurate as of August 2026;
re-verify names and positioning before relying on it.

One sentence per row. OpenAI's Agents SDK is the simplest of the four to
read — Agent plus Runner, with handoffs, guardrails, and sessions as its
distinctive additions. Anthropic's Claude Agent SDK is the same harness
that runs Claude Code, with a notably strong tool-permission model.
Google ADK is Gemini's code-first framework, with unusually good
evaluation hooks. AWS Bedrock AgentCore is a managed runtime with the
enterprise deployment and IAM story — the one an infrastructure team
asks about first, because finance shops are AWS-heavy, Envestnet
included.

None of these were built on today for a structural reason, not a quality
one: every provider SDK assumes a hosted frontier model on the other end,
and this room runs offline. The row that matters most in any given shop
is the one matching the cloud already under contract.
-->

---

# M8.4.6 · Open Source, Model-Agnostic

| Framework | Shape | Distinctive |
|---|---|---|
| LangGraph | explicit state graph | industry default, max control |
| CrewAI | role-based crews | fast demo path, harder to inspect |
| PydanticAI | typed agents | your M7 contracts ARE the API |
| LlamaIndex | tools + indexes | agents and RAG share a toolbox |
| smolagents | minimal HF loop | built for small local models |

<!--
DRAFT — facts that rot; re-check positioning against each framework's
current release before relying on it.

Four of these five rows appeared earlier today, which is what makes the
table readable rather than a list of brands: LangGraph's "explicit state
graph" is M8.3.4, PydanticAI's "contracts are the API" is M8.3.2,
LlamaIndex's shared toolbox is M8.3.3, smolagents' minimal loop is
M8.1.2. The one unmet row is CrewAI: agents as role-played coworkers
(researcher, analyst, writer) declared in YAML-ish config — the fastest
path to an impressive demo and the hardest of the five to inspect when
something goes wrong, which is why it did not earn a build slide.

Also in this family, worth knowing by name: Microsoft AutoGen / Agent
Framework, Semantic Kernel, Haystack. The evaluation method is always the
same — the M8.4.2 checklist and the M7.3.7 questions.
-->

---

# M8.4.7 · Why Today Ran The Way It Did

Criteria: simple API · runs a **local** model · typed tools · inspectable

| Track | Framework | Why |
|---|---|---|
| **Ran + built** | **smolagents** | only one that runs SmolLM2 offline |
| **Read** | PydanticAI, LlamaIndex, LangGraph | recognition, with a key |

Reading four costs minutes. Building in four costs your week.

<!--
The choice slide, run in reverse: instead of promising a decision
process, it explains the day that just happened as the output of one. The
criteria — simple API, runs a local model, typed tools, inspectable —
were applied to the real constraint of this room: no HuggingFace access,
no API keys, so the only live planner available is the committed
SmolLM2-135M. smolagents is the framework designed for exactly that model
class, so it was the one to build in; the other three cost minutes to
read and would cost a week each to build in, hence the two-track day.

The disclaimer is part of the content: this is not "smolagents is the
best framework." At a desk with an API key, PydanticAI or LangGraph may
serve better. The transferable part is the method — name the constraints,
derive the criteria, then choose from the requirements.
-->

---

# M8.4.8 · The Day In One Picture

```text
M7    you wrote the loop        60 lines, yours
M8.1  a framework ran it        15 lines, wrong answer
M8.2  a workflow got it right   same model, right answer
M8.3  three frameworks read     one lens: where's my runtime?
M8.4  the map                   criteria, not brand preference
```

Three things to keep:

- Frameworks package the loop **you already wrote**
- Planner quality gates agent quality
- **Least autonomy that works**

Tomorrow, M9: memory, approval, streaming — and this agent moves into Chronos.

<!--
The day in one picture: the same question
went from wrong (autonomous agent, tiny planner) to right (workflow, same
tiny planner), and every framework read along the way turned out to be
the M7 runtime wearing a different coat. The three keepers at the bottom
compress the whole module — frameworks package the loop already written;
planner quality gates agent quality; least autonomy that works.

The M9 line is a promise, not a summary: tomorrow this exact workflow
gains memory, persistence, a human approval gate, and a place in the
Chronos advisor dashboard. From here, straight into the lab.
-->

---

<!-- _class: lead -->

# M8.L1 · Lab: Ship The Assistant Into Chronos

**Warm-up (10 min)** — the patterns, on toy data:

```bash
cd CODE-ALONGS && uv sync --extra agents
uv run python -m m8.smolagents_agent
uv run python -m m8.pattern_chaining
```

**Main event** — implement the starter pack:

`labs/m8_advisor_assistant/` — five stubs, 15 failing tests.
Make them green; ship a routed, fact-grounded, rule-checked
advisor note into the Chronos API.

<!--
The lab rule changes today: the warm-up is assembly, the main event is
engineering. The code-along files are toys — hardcoded prices, dict
tools — and nothing in them pastes into the capstone, where the same
patterns meet real Pydantic schemas, a real database session, and the
point-in-time price rule. Same shapes, different substance. Understanding
the morning is enough to DESIGN this feature; the lab is WRITING it.

The API endpoint for this feature already
exists and currently answers 501 "complete the M8 lab" — the code built
in this lab is what makes it respond. It is also a foundation, not a
throwaway: tomorrow (M9) this exact feature gains memory, a human
approval gate, and a place in the advisor dashboard.
-->

---

# M8.L2 · The Feature In One Picture

```text
POST /advisor/clients/{id}/assistant   {"question": ...}
        |
  route_client_question      front door    (M8.2.3)
        |-- "trade" --> REFUSE, no data touched
        |-- "policy" -> answer from thresholds
        |-- "portfolio"
             |
  gather_client_facts        existing read paths
             |
  judge_against_guidelines   Python owns the verdict
             |
  draft_advisor_note         SmolLM2 or template
             |
  review_advisor_note        rule gate, 1 revision
             |
  AdvisorAssistantAnswerResponse (a DRAFT for M9)
```

<!--
Every box maps to a pattern slide from this morning — route (M8.2.3),
chain (M8.2.2), evaluator (M8.2.5) — but now the boxes are files in a
business-named package, one function per file: the M0 naming rule at
work. Nothing in this picture is new; the lab is assembling known pieces
against real data.

Two boxes deserve a pause. gather is SEQUENTIAL, not the M8.2.4 fan-out:
these lookups share one SQLAlchemy session, and sessions are not
thread-safe — the parallel pattern belongs to independent services with
their own connections, and recognizing when NOT to apply a pattern is
the judgment this module keeps asking for. And the response is a DRAFT
because M9 puts a human approval gate between this note and any
client, so the type is shaped for tomorrow before tomorrow arrives.
-->

---

# M8.L3 · The Interfaces You Implement

```python
route_client_question(question: str) -> str
    # "portfolio" | "policy" | "trade"

gather_client_facts(db, client_user_id)
    # -> (PortfolioResponse, AdvisorMetricResponse,
    #     recommendations: list[str])

judge_against_guidelines(metrics) -> str

draft_advisor_note(question, metrics, verdict,
    recommendations) -> (note, note_source)

review_advisor_note(note, verdict) -> list[str]

answer_client_question(db, client_user_id,
    question) -> AdvisorAssistantAnswerResponse
```

Each is a stub in `labs/m8_advisor_assistant/` — with hints.

<!--
The contract slide — what to build, not how. The starter pack draws a
deliberate line: plumbing that was NOT today's lesson
(gather_client_facts, model_loading) is given complete; the five
functions that WERE today's lesson are stubs with docstring hints. The
raw material all exists in chronos already — facts from
build_current_portfolio_snapshot and analyze_client_portfolio,
thresholds from advisor_workspace (the same 35% met three times today).
The lab instructions document carries the step order and acceptance
checks; the slides stay interface-only, because writing the functions is
the exercise and transcribing them would not be.

No answer key is included — solutions live in an instructor-only, gitignored
folder. The motivation is structural instead: the API endpoint serves
the labs package directly, answering 501 "complete the M8 lab" until the
stubs are implemented. Green tests mean a live feature.
-->

---

# M8.L4 · The Rules You Inherit

| Rule | Where it already lives |
|---|---|
| Works with no key, no model | template `note_source` |
| LLM never calculates | facts + verdict pre-computed |
| Cannot mutate portfolios | no trading import exists |
| No future prices | `build_current_portfolio_snapshot` |
| Tests never touch network | `tests/fixtures/` |

The agent is new. The guarantees are not.

<!--
The capstone's non-negotiables, restated as inherited properties: build
the package by composing existing read paths, and every rule holds with
no extra effort. The middle row is the important one — the model receives
the verdict already decided, which is exactly how the morning's chaining
slide fixed the trace; the safety rule and the reliability pattern are
the same design choice. "Cannot mutate portfolios" holds by construction, not
by policy: no trading function is importable from the package, the M7
lesson of never registering the dangerous tool. And the last row is why
the lab is checkable anywhere: the whole workflow runs offline on the
fixture prices with note_source == "template", no model required.
-->

---

# M8.L5 · Success Criteria

```bash
cd CAPSTONE-PROJECT/chronos_wealth_management
uv run python -m pytest labs/m8_advisor_assistant -q
```

15 tests, ordered by build step — the last two over HTTP:

- Trade-shaped question → `refused=True`, **no data accessed**
- Portfolio question → verdict + note citing the threshold
- No model installed → `note_source == "template"`, still correct
- Investor calling the endpoint → `403`

Then: `uv sync --extra agents` and watch `note_source` change.

<!--
The test file is included with the lab: 15 offline tests, ordered by build
step, pinned to the deterministic template path so results are identical
with or without a model installed. The final command shows the upgrade
path: the SAME feature, template note before, SmolLM2 prose after,
zero code change — the draft function is the swap point, and the same
swap is how a cloud model arrives after the workshop.

A gotcha that costs real debugging time: run tests as
`uv run python -m pytest`. When the venv and extras drift out of sync,
bare `uv run pytest` can silently fall back to a pytest found on PATH
(conda, typically) running the wrong Python entirely, and the failures
look like nonsense.

Two live-run details are worth calling out. A freshly seeded Alice is
100% cash, so the first verdict is the 40% CASH breach — the 35%
concentration verdict appears only after Alice buys AAPL heavily, and
two different breaches exercise the same workflow. Also,
SmolLM2's prose will be mediocre while every figure stays correct,
because Python computed the figures and the model only phrased them —
the chaining separation, visible live.
-->

---

# M8.L6 · Stretch Options

- Upgrade the keyword router to BGE embeddings — then test
  "How much cash would selling AAPL raise?" against both
- Add `elapsed_ms` per workflow step (M7's trace habit)
- Point the smolagents code-along at the real Chronos API
- Read `answer_client_question` and list what M9 must add:
  memory, approval, streaming

Only after the required path is green.

<!--
Each stretch extends a thread from the day. The first closes the
morning's loop with a useful contrast: the embedding router
MISROUTES the sell-euphemism question from M8.2.9, while the keyword
router refuses it correctly — sophistication is not safety, and
the engineering question is what would make the embedding router safe
(more examples? a margin threshold? both?). The elapsed_ms stretch
carries M7's telemetry habit forward; the Chronos-API stretch connects
the code-along world to the real one.

The last stretch is tomorrow's agenda, discoverable by reading today's
code: answer_client_question accepts a conversation_history parameter
that nothing uses yet. An accepted-but-unused parameter, a response
framed as a draft, a single swappable draft function — those are the
extension points M9 uses.
-->
