---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M9 · Finishing Agentic Applications

M7 built the loop.

M8 built the workflow.

M9 turns it into a product-safe LlamaIndex feature.

By the end of this module you can:

- add bounded conversation memory
- route follow-up questions with context
- verify generated drafts with rules and a model judge
- put client-facing output behind a human approval gate
- persist the state and trace that must survive restart

---

<!-- _class: lead -->

# M9.1 · From Agentic Workflow To Product Feature

M8 got us here:

```text
question
  -> route
  -> gather tool facts
  -> search policy
  -> check guideline
  -> draft answer
  -> trace result
```

That is an agentic workflow.

It is not yet a finished product feature.

---

# M9.1.2 · What Is Still Missing

The M8 assistant can answer one request.

It still needs:

- memory for follow-up questions
- bounded history so context does not grow forever
- verification of generated drafts
- a human gate before client-visible output
- durable state for drafts, decisions, and trace

M9 adds these with LlamaIndex without changing the M7/M8 mental model.

---

# M9.1.3 · Watch It Forget

Two requests in a row:

```text
Q1: What does the concentration guideline say?
    route: policy -> 35% threshold

Q2: Why is that a problem for Alice?
    route: unclear without history
```

The follow-up only makes sense because of Q1.

Without memory, the app answers an orphan.

---

# M9.1.4 · The Product Rule

An agentic app is not done when the model answers.

It is done when the system can explain:

- what the user asked
- which facts and tools were used
- what the model drafted
- which checks passed or failed
- who approved client-visible output
- what state survives a restart

---

<!-- _class: lead -->

# M9.2 · LlamaIndex Memory For Follow-Ups

Memory is not inside the model.

In LlamaIndex, memory is still the transcript the app sends again.

```text
history + new question -> next model call
```

Code: `CODEALONGS/m9_memory_verification_hitl/01_memory_is_messages.py`

---

# M9.2.2 · Bounded Memory

Appending forever is not a product design.

```text
full history       exact, expensive, unbounded
windowed history   exact recent turns, bounded
summary            compact, lossy
retrieval memory   long-term store, RAG again
```

Start with a LlamaIndex memory window.

Code: `CODEALONGS/m9_memory_verification_hitl/02_bounded_memory.py`

---

# M9.2.3 · Keep, Fold, Or Store

Three ways to bound memory:

| Strategy | Trade-off |
|---|---|
| window | exact recent turns, older context gone |
| summarize | compact, fluent, silently lossy |
| retrieve | long-term memory, same hard problems as RAG |

Start with a window.

Add summaries or retrieval only when the failure requires it.

---

# M9.2.4 · Effective Question

A follow-up is often an orphan:

```text
"Why is that a problem for Alice?"
```

Route on the conversation, not the orphan:

```text
history: "What does the concentration guideline say?"
latest:  "Why is that a problem for Alice?"
route:   policy
```

Code: `CODEALONGS/m9_memory_verification_hitl/03_effective_question.py`

---

# M9.2.5 · Memory Scope

Memory must not out-privilege the fresh request.

Keep memory scoped by:

- advisor
- client
- workflow
- role permissions

Never let Alice's transcript help answer Bob's question.

---

<!-- _class: lead -->

# M9.3 · Verification Ladder

One job:

```text
Is this generated work good enough to move forward?
```

Three rungs:

```text
rules        cheap, deterministic, predicted failures
model judge  one more model call, fuzzy quality
human        expensive, catches what nobody predicted
```

They stack.

---

# M9.3.2 · Rung 1: Rules

Rules should check the LlamaIndex-generated draft before any judge or human sees it.

Examples:

- note is short enough
- blocked verdict cites the threshold
- required source or fact appears
- forbidden action is absent

Rules are not enough, but they are always worth having.

Code: `CODEALONGS/m9_memory_verification_hitl/04_verify_generated_draft.py`

---

# M9.3.3 · Rung 2: Model Judge

A judge is another LlamaIndex model call.

Ask one closed question:

```text
Does this note cite a specific threshold percentage?
Answer YES or NO.
```

Then compare it with a known rule.

The judge starts advisory. It earns veto power with measured data.

Code: `CODEALONGS/m9_memory_verification_hitl/05_model_judge.py`

---

# M9.3.4 · A Judge Is Only As Good As The Judge

A model judge is not truth.

It is another model call.

Before it gets authority, measure it:

```text
known note -> rule label -> judge label -> agreement
```

Use the judge as advisory until it earns trust.

Bad judges create confident approval theater.

---

# M9.3.5 · Least Oversight That Works

Use stakes to choose the rungs:

```text
rules       every output
judge       high volume, fuzzy quality, survivable errors
human       client-facing, money-moving, regulator-visible
```

M8 taught least autonomy that works.

M9 adds least oversight that works.

---

# M9.3.6 · What Finishing Costs

Finishing an agentic feature adds real cost:

```text
memory       more tokens every turn
judge        one more model call per draft
human gate   review time and queue operations
state        durable rows and audit trails
trace        storage plus replay discipline
```

Oversight is not decoration.

It is part of the application budget.

---

<!-- _class: lead -->

# M9.4 · Human Gate, State, And Trace

Generated client-facing content from the M8 workflow should become a draft.

Not a message.

```text
assistant drafts -> pending
advisor reviews  -> approved | rejected
client sees only approved
```

Code: `CODEALONGS/m9_memory_verification_hitl/06_human_gate_and_state.py`

---

# M9.4.2 · Draft State Machine

Keep the state machine small:

```text
pending -> approved
pending -> rejected
```

Important invariants:

- draft creation always starts at `pending`
- only the decision function can approve
- decisions are final
- rejected content is never client-visible

---

# M9.4.3 · Why The Rejection Path Matters

Approval proves the happy path.

Rejection proves the safety property.

```text
advisor rejects draft
client dashboard shows nothing
```

The absence is the feature.

---

<!-- _class: lead -->

# M9.4.4 · Production State, Recovery, Trace

State that matters must survive process death.

```text
conversation memory   may be session state
pending drafts        durable rows
human decisions       durable rows
audit trace           durable rows/logs
```

Code: `CODEALONGS/m9_memory_verification_hitl/06_human_gate_and_state.py`

---

# M9.4.5 · What To Keep In The Trace

For each agentic run, keep:

- original question
- effective question
- route
- facts/tool observations
- generated draft
- rule review
- judge verdict
- approval decision
- stop reason

If you cannot replay the trace, you cannot debug the agent.

---

# M9.4.6 · The Finished Feature

End-to-end closure:

```text
history
  -> effective question
  -> route
  -> gather/search/check facts
  -> SmolLM drafts answer
  -> Python rules verify
  -> SmolLM judge advises
  -> pending approval row
  -> human approves
  -> client sees approved note
```

Code: `CODEALONGS/m9_memory_verification_hitl/06_human_gate_and_state.py`

---

<!-- _class: lead -->

# M9.5 · Agentic Chapter Closure

```text
M7  the loop, by hand      model proposes, Python executes
M8  the workflow           tools, RAG, frameworks, patterns
M9  the finished feature   LlamaIndex memory, verification, gate, state
```

The chapter closes here:

```text
remember -> verify -> gate -> persist
```

Tomorrow: its tools are still hardwired. **MCP.**

---

<!-- _class: lead -->

# M9.5.2 · Lab: Everything You Built, Gated

Build the production closure around the M8 assistant:

```text
submit_note_for_approval   draft intake
decide_note_draft          human decision
answer_with_memory         follow-up memory
judge_note_with_model      stretch judge
```

Gate first. Memory second. Judge as stretch.

---

# M9.5.3 · Success Criteria

```bash
cd CAPSTONE-PROJECT/chronos_wealth_management
uv run python -m pytest labs/m9_advisor_assistant -q
```

The live loop should prove:

- ask -> pending draft
- approve -> Alice sees the note
- reject -> Alice never sees it
- restart -> pending queue survives
- follow-up -> route stays on thread

Shipped suite stays green: `uv run python -m pytest -q`
