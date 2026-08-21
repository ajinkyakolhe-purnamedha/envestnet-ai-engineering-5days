---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M3.0 · AI Application Patterns

M0 gave you maintainable Python. M1 gave you model capability. M2 exposed a
call's context, cost, and limits.

Now choose the least-complex reliable application pattern.

- Separate model, instruction, context, and prompt
- Choose a model and deployment boundary for the task
- Choose the first rung that satisfies the requirement
- State why a simpler rung fails
- Add a deterministic boundary before trusting output

<!--
M3 is an architecture decision module, not a framework catalogue. Chronos is
the shared synthetic reference implementation; the pattern applies equally to
support, operations, document, and internal-workflow applications. M4, M6,
M7/M8, M13 and M14 build the deeper systems named here but not implemented.
-->

---

# M3.1 · Keep four things separate

| Thing | Question it answers | Owned by |
| --- | --- | --- |
| Model | What language capability is available? | provider / deployment |
| Instruction | How should it behave? | application |
| Context | What facts are available now? | application / data boundary |
| Prompt | What assembled request is sent? | application |

Confusing these makes failures hard to diagnose.

---

# M3.1 · Assemble the request visibly

```python
def assemble_prompt(instruction, context, question):
    return f"INSTRUCTION: {instruction}\nCONTEXT: {context}\nQUESTION: {question}"
```

If tone is wrong, inspect the instruction. If a fact is wrong or missing,
inspect the context. If the call is malformed, inspect assembly.

Source: `CODEALONGS/day_1/m3_application_patterns/01_assemble_prompt.py`

<!--
This boundary helps students stop saying “the prompt failed.” Ask which input
actually owns the observed failure. The model is one component, not the whole
application.
-->

---

# M3.1 · Checkpoint: diagnose the failure first

Change the instruction and then change the context.

1. Which change should alter tone?
2. Which change should alter the answer's available facts?
3. Which failure belongs to a Python business rule instead?

Try it in: `CODEALONGS/day_1/m3_application_patterns/01_assemble_prompt.py`

---

# M3.2 · Model selection is an operating decision

```text
task → quality → cost → latency → data boundary
     → ownership → serving effort
```

The best benchmark score is not automatically the best product choice.

Choose the smallest capable model and the simplest operating boundary that meet
the workflow's constraints.

<!--
M1 introduced ways to access models. Here, turn that inventory into an
engineering decision. Do not begin with a provider or a favourite model name.
Begin with the task and the constraints under which it must operate.

The outcome is a written selection rationale, not a claim that one model wins
all tasks. M2 provided the context, cost, and latency evidence used here.
-->

---

# M3.2 · Open models: family before version

Examples include Qwen, Llama, Mistral, and Gemma families.

- A family has a characteristic capability, license, and operating shape
- A version changes quickly; read the current model card before committing
- Check license, modality, context, hardware, and evaluation evidence

Open weights can improve control and portability; they also make you own more
of serving, upgrades, safety, and evaluation.

<!--
Avoid a leaderboard. The durable habit is to understand a family and inspect a
specific release only when a feature has real requirements. A model card is a
delivery artifact: confirm license terms, supported modalities, context limit,
hardware needs, and known limitations before procurement or implementation.

Open weights do not mean that everything is open. Weights, training data,
licence, and distribution rights can all have different boundaries.
-->

---

# M3.2 · Size is one dial

```text
task fit + supplied context + prompting + model size
                 + deployment + evaluation
```

More parameters can improve capability, but size is not an intelligence score.

- A small model can excel at a narrow, supplied-context task
- A larger model may still fail without facts, tests, or permissions
- Mixture-of-experts models make raw parameter counts especially imperfect

<!--
Keep this connected to M2. Bigger models commonly cost more and take longer,
but parameter count alone does not tell learners whether a model will solve the
task. Training data, post-training, model architecture, the supplied context,
and the desired output shape all matter.

The practical question remains: what is the smallest capable choice that passes
the tests for this workflow?
-->

---

# M3.2 · What size buys

| Tier | Open-weight size* | Good first use |
| --- | --- | --- |
| Small / local | 0.1B–3B | tagging, extraction, simple rewrite |
| Workhorse | 7B–32B | supplied-context Q&A, summaries, tools |
| Frontier-sized | 70B+ | difficult reasoning, complex coding |

*For mixture-of-experts models, total parameters ≠ active parameters per token.

Start at the lowest tier that can pass a representative test set. Escalate with
evidence—not because a larger model sounds safer.

<!--
The bands are approximate open-weight model sizes, not a benchmark leaderboard.
Exact parameter counts become stale quickly, and parameter count is not
comparable across every architecture. In mixture-of-experts models, total
parameters can be large while only part of the model is active for each token.
The table gives learners a starting hypothesis to test.

For Chronos, a template or small local model may be sufficient for a narrow
advisor-note rewrite; difficult cross-document reasoning likely needs a more
capable boundary plus retrieval and evaluation.
-->

---

# M3.2 · Closed models change the operating model

```text
no download → no GPU → one HTTP call
```

You gain fast access to capability and reduce infrastructure work.

You also send permitted prompt data across a service boundary and pay for
input/output tokens. Quality goes up; the operating model changes.

<!--
This is not an argument against closed services. They are often the fastest
path to a useful feature. The point is that the model no longer runs in the
application's environment: identity, data handling, usage, token bills,
availability, and provider terms become system concerns.

In a regulated workflow, ask which data may cross the boundary and under what
contract before asking which model is strongest.
-->

---

# M3.2 · Service boundaries trade different things

| Boundary | You gain | You take on |
| --- | --- | --- |
| Direct provider API | fastest access | API-key/data boundary, token bill |
| Cloud model platform | IAM and governance | account, region, billing setup |
| Hosted open-weight API | model choice | provider evaluation and portability risk |

There is no universally right boundary. Choose one that fits the task, data,
organisation, and delivery constraints.

<!--
Examples change quickly, so do not turn this into a vendor comparison. A direct
provider API is normally fastest to prototype. A cloud platform adds enterprise
identity, audit, billing, and regional controls. Hosted open-weight inference
offers model choice without operating GPUs, but the provider still forms a data
and availability boundary.
-->

---

# M3.2 · Match the model to the job

| Model kind | Use it when | Example |
| --- | --- | --- |
| Specialist | one modality or narrow task dominates | embedding search, reranking, speech |
| General-purpose | language work is the core workflow | draft, extract, classify, explain |
| Multimodal | the evidence includes images, audio, or documents | chart, statement, call recording |

Do not pay for broad capability when a specialised model reliably solves the
task. Do not force a specialist to perform a general reasoning workflow.

<!--
This is a second selection axis independent of size. An embedding model may be
small and superb at retrieval but cannot draft an advisor note. A multimodal
model is valuable when a chart or PDF is actual evidence, not merely because it
has more features.

The selection document should name task modality, quality target, context/data
boundary, latency and cost budget, and why this model kind is sufficient.
-->

---

# M3.3 · The five-pattern ladder

| Pattern | Adds | Use when |
| --- | --- | --- |
| Direct call | general language capability | drafting, rewriting, translation |
| Prompted application | instruction, format, constraints | extraction or controlled shape |
| RAG | retrieved facts and citations | current/private/document knowledge |
| Fine-tuning | learned repeated behaviour | stable high-volume task or style |
| Agentic workflow | dynamic tools and steps | steps genuinely vary |

Every rung adds capability—and new failure modes to own.

---

# M3.3 · Pattern 1 — Direct call

```python
messages = [
    {"role": "system", "content": "You are a concise advisor assistant."},
    {"role": "user", "content": "Explain the risk in a portfolio with 52% in AAPL."},
]

reply = call_smolm(messages)
```

Use it for a self-contained language task such as rewriting a supplied adviser
note, support reply, or internal update. Its failure is unsupported facts or
output that a downstream system cannot safely consume.

Source: `CODEALONGS/day_1/m3_application_patterns/02_direct_llm_call.py`

<!--
Direct is a valid pattern, not a beginner's mistake. It is the correct starting
point when the task needs general language capability and no current/private
facts or structured downstream action.
-->

---

# M3.3 · Pattern 2 — Prompted application with Structured Output

```python
class TradeIntent(BaseModel):
    action: Literal["buy", "sell"]
    symbol: str
    shares: int = Field(gt=0)

intent = client.create(response_model=TradeIntent, messages=messages)
```

Use Instructor plus Pydantic as the primary implementation: the application
requests a typed response rather than hoping a prose parser succeeds.

Source: `CODEALONGS/day_1/m3_application_patterns/03_prompted_extraction.py`

<!--
Show Instructor and Pydantic as the teaching boundary. The cookbook snippet
keeps the first concept small—the schema—while a production client call injects
the model client and uses `response_model=TradeIntent`. Do not introduce a
parallel provider-native structured-output API here.
-->

---

# M3.3 · Schema validation is not business validation

```python
def validate_trade_request(payload):
    return payload["symbol"] in {"AAPL", "SPY", "QQQ"} and payload["allocation_percent"] <= 35
```

A typed `TradeIntent` means the data has the expected shape. It does **not**
mean the requester is authorised, the fact is current, or the action is safe.

The trade is only the shared example: the same boundary applies to a ticket,
claim, request, or workflow hand-off.

Python policy, permissions, and approval controls remain application-owned.

<!--
This is the critical failure after Pattern 2: valid JSON is not a valid business
action. Instructor/Pydantic validate the schema; deterministic application
rules validate the action. Keep the distinction explicit.
-->

---

# M3.3 · Pattern 3 — RAG

Add retrieved facts and citations when the answer depends on current, private,
or document-bound knowledge.

- Direct model knowledge is not a governed policy source
- Prompting cannot make missing documents appear
- Retrieval adds indexing, relevance, citations, and evidence checks

Deep implementation belongs to M4.

Source: `CODEALONGS/day_1/m3_application_patterns/04_simple_rag_architecture.py`

<!--
Use the M2 embeddings preview as the bridge. RAG is named here as an
application pattern; keep implementation to retrieve -> prompt -> answer.
M4 owns LlamaIndex, indexes, chunking, retrieval tuning, and grounded answers.
-->

---

# M3.3 · Pattern 4 — Fine-tuning

Add learned repeated behaviour only when a prompt/RAG baseline has evidence of
a persistent gap on a stable, high-volume task.

- Needs representative labelled examples
- Adds training, versioning, serving, and regression risk
- Does not replace current/private facts

Deep implementation belongs to M6.

---

# M3.3 · Pattern 5 — Agentic workflow

Add dynamic tool selection and multi-step control only when the steps genuinely
vary at runtime.

- Adds tool permissions, loops, traces, and blast radius
- A fixed sequence is usually ordinary Python orchestration
- “Agent” is not a reward for a complicated diagram

Deep implementation belongs to M7 and M8.

---

# M3.4 · Choose the first rung that works

```text
general language only?               → Direct call
needs controlled shape or constraints? → Prompted application
needs current/private facts?         → RAG
needs learned stable behaviour?      → Fine-tuning
needs dynamic steps/tools?           → Agentic workflow
```

Start with the smallest pattern that meets the requirement, then earn each
extra layer with observed failure evidence.

---

# M3.4 · A selection is a written argument

For every proposed application, write:

```text
data needed → likely failure → simplest pattern
→ deployment/model boundary → why not simpler → first test
```

The word “agent” or “RAG” is not an answer until it has this argument.

<!--
This makes architecture review concrete. Insist on “why not simpler”; it keeps
the module from becoming a technology shopping list.
-->

---

# M3.4 · Checkpoint: three application cases

| Candidate | First likely pattern | Question to defend |
| --- | --- | --- |
| Rewrite a supplied client note | Direct call | Why is a response schema unnecessary? |
| Extract a support-ticket hand-off | Prompted application | Why is prose unsafe downstream? |
| Answer from changing internal policy documents | RAG | Why cannot model memory be the source? |

Try it in: `CODEALONGS/day_1/m3_application_patterns/05_choose_pattern.py`

---

# M3.5 · Deterministic contracts come first

```python
assert not validate_trade_request({"symbol": "AAPL", "allocation_percent": 36})
```

Use ordinary Python for facts that have an exact answer: policy caps, required
fields, permitted symbols, citation presence, and authorization boundaries.

Source: `CODEALONGS/day_1/m3_application_patterns/06_test_contract.py`

<!--
The model can propose; deterministic application code decides what is allowed.
Fuzzy quality evaluation matters too, but it comes after the simple reliable
contracts and has dedicated later coverage.
-->

---

# M3.5 · Checkpoint: test the boundary, not the model's confidence

Try a permitted allocation, an over-cap allocation, and an unknown symbol.

- Which result can be asserted exactly?
- Which concern needs later evaluation rather than a Boolean test?
- Why should a model not be its own final policy judge?

Try it in: `CODEALONGS/day_1/m3_application_patterns/06_test_contract.py`

---

# M3.L · Mini lab: one choice card

Choose one: extract a proposed trade, create a support-ticket hand-off, or
answer a question from changing policy documents. Then fill:

1. Data needed
2. Likely failure
3. Simplest pattern
4. Model/deployment boundary
5. First deterministic test

Source: `CODEALONGS/day_1/m3_application_patterns/lab/mini_lab.md`

---

# M3.L · Main lab: Chronos selection clinic

For three candidate applications—one wealth-management, one operations or
support, and one document/private-knowledge workflow—produce one decision
table with:

```text
candidate | workflow | data boundary | pattern | model tier
why not simpler | first test
```

Implement only one tiny direct-call or prompted-extraction example. Leave RAG,
fine-tuning, and agentic implementation to their owning modules.

Acceptance: every row has a real data boundary, the least-complex fitting
pattern, a concrete reason a simpler choice fails, and one observable test.

Lab pack: `CODEALONGS/day_1/m3_application_patterns/lab/`

<!-- **Instructor only:** timebox to 60–90 minutes and ask each group to defend why not simpler before discussing tools. -->

---

<!-- _class: lead -->

# M3.6 · Day 1 closes with a design discipline

Build maintainable Python.
Use models through an explicit boundary.
Measure context and cost.
Choose a model boundary for the task.
Choose the first application pattern that works.
Test deterministic rules outside the model.

Apply this discipline to any workflow: identify the data boundary, choose the
least-complex pattern, and test deterministic rules outside the model.

Next: M4 turns the RAG decision into a grounded application with documents,
retrieval, citations, and evaluation.
