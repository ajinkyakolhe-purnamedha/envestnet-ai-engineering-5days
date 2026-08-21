---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M1.0 · Introduction to AI Models

From model capability to AI applications

By the end of this module, you can:

- Explain why the largest AI opportunity is in applications
- Call a proprietary model and run an open-weight one locally
- Put a model behind a small, logged application boundary
- Say where a model call will live once your organisation owns it

<!--
This module is the bridge from M0 Python to the rest of AI engineering. The
throughline is a synthetic portfolio assistant: one shared implementation
example, not the scope of the course. The model is impressive, but the
application is what makes it useful in any workflow.

The module has one shape: argue that the application is the opportunity
(M1.1), then build toward one — call a model (M1.2), run a model (M1.3),
choose between them (M1.4), assemble the assistant (M1.5), extend it in the
lab, and only then show where this runs in an enterprise (M1.6).

**Instructor only:** reserve roughly half the module for M1.2 onward. The
opening argument is five slides and should move quickly — the visuals carry
it, not the text.
-->

---

# M1.1.1 · AI models can work with many kinds of information

**Language** — write, summarise, extract, translate, classify, reason, code

**Vision** — read images, charts, screenshots, and documents

**Audio** — transcribe speech and generate speech

**Generation** — create images, video, and audio

**Action** — select tools and trigger workflow steps

```text
A model can generate an answer.
An AI application must make that answer
useful, safe, and affordable.
```

<!--
Capability is real, but it is not the end of the engineering problem. A useful
application needs permitted context, a workflow, evaluation, safety, cost
control, and operations.

**Instructor only:** an optional 2-minute demonstration: ask a model to name
the greatest concentration risk in a synthetic portfolio note.
-->

---

# M1.1.2 · AI becomes useful where work already happens

| Standalone chat | AI inside the work |
|---|---|
| Ask a generic question | Explain a client's portfolio change or a support exception |
| Paste documents manually | Read permitted policy or product documents |
| Copy a result elsewhere | Draft a review inside the workflow where work happens |

Examples such as a financial-analysis Project or a document-grounded notebook
show the same transition: capability becomes useful when it meets real work.

<!--
The example does not endorse a particular product. It shows the interaction
shift: context is supplied safely and automatically, and the result appears
where the user already makes decisions.
-->

---

# M1.1.3 · Model families and the capability landscape

| Category | Examples to know | General lesson |
|---|---|---|
| Proprietary frontier models | Gemini, GPT, Claude | Fastest route to broad capability |
| Open-weight generalists | Qwen, Llama, DeepSeek, Mistral | More portability and deployment control |
| Specialists | Speech-to-text, image, embeddings, reranking | Smaller, faster, cheaper, often better at one job |

Model names change quickly. The engineering skill is recognising the category
and choosing it for the task.

<!--
These are dated examples, not a leaderboard. Explain that open weights do not
automatically mean open training data or an unrestricted licence.

The specialist row matters more than it looks: transcription wants a speech
model, semantic search wants an embedding model, and neither wants a frontier
chat model. We meet embeddings again in M2 and reranking in M5.

**Instructor only:** if time allows, one speech-to-text and one text-to-image
demonstration lands this row. They are demonstrations, not learner setup —
hosted availability, quotas, and authentication change frequently.
-->

---

# M1.1.4 · A model is not a product

| Manual model use | Product feature |
|---|---|
| A person pastes data into chat | The application receives permitted workflow data |
| A person writes the prompt | Code supplies instructions consistently |
| A person decides whether to trust it | The application evaluates and shows limits |
| A person copies the result elsewhere | The result appears in the workflow itself |

A model does not know your customers, your policies, your systems, which data
it may use, or what a correct answer means here.

> A product is model + data + workflow + safety + evaluation + operations.

<!--
Use the supplied "model as infrastructure" visual here. The same model can be
used manually or embedded in an application; the difference is engineering.

This is also the course map. Every later module adds one term to that
equation: M2 context, M3 pattern choice, M4/M5 retrieval and its evaluation,
M6 adaptation, M7-M9 tools and oversight, M10-M12 integration, M13-M15
testing and operations.
-->

---

# M1.1.5 · Every platform creates an application wave

```text
Computers created software companies.
The internet created web applications.
Cloud created SaaS applications.

AI creates a new application layer.
```

Every repeated **question, decision, document, review, search, and hand-off**
is a candidate: an advisor copilot for a portfolio review, a support assistant
for triaging an exception, a policy assistant for extracting constraints.

> The model may be shared by everyone. The application is what you build.

<!--
Use the strongest of the supplied historical-platform visuals here. The
durable lesson does not depend on a specific market-revenue ratio: as
infrastructure becomes available, builders create applications that solve
previously uneconomic or impossible problems.

The point is possibility, not that every workflow should be automated. The
next question is practical, and the rest of the module answers it: how do we
reach a model from an application?
-->

---

# M1.A · Find an AI application opportunity

Choose one repeated question, decision, document task, review, search, or
workflow hand-off. Describe:

```text
User:
Current manual workflow:
AI capability needed:
Data required:
What makes a good answer:
```

Keep it as a candidate. M3 will decide whether it needs a prompt, RAG,
fine-tuning, an agent, or none of these.

<!--
This is a 10-minute individual or small-group activity. The output is a useful
candidate backlog, not a solution design. **Instructor only:** capture the
examples so later modules can refer back to real learner opportunities.
-->

---

# M1.2.1 · Three ways to reach a model

| Path | Example | What changes |
|---|---|---|
| Proprietary, direct | Gemini, GPT, Claude API | Fastest path from Python to a model |
| Open weights, local | SmolLM2 on this laptop | No key, no network, no per-call bill |
| *Through your cloud* | *Vertex, Bedrock, Azure* | *Project, identity, billing, governance* |

Ask the same questions every time: **task, quality, cost, data boundary,
ownership, and serving effort.**

<!--
Say the third row out loud and then set it aside: in your organisation the
call will almost certainly run through Vertex or Bedrock, and we cover that in
the last section. For now we call directly, because the mechanics are the
thing being taught and a governed boundary hides them.

Expect the objection early — "we are not allowed to put an API key in a
script." Agree with it, point at M1.6, and move on.

Use "open weights" precisely: weights may be available while training data,
training pipeline, and licence terms remain different.
-->

---

# M1.2.2 · Three proprietary SDKs, one identical shape

```python
def call_gemini(prompt):
    client = genai.Client(api_key=key)
    reply = client.models.generate_content(
        model="gemini-3.5-flash-lite", contents=prompt)
    return reply.text

def call_openai(prompt):
    client = OpenAI(api_key=key)
    reply = client.responses.create(
        model="gpt-5-mini", input=prompt)
    return reply.output_text

def call_claude(prompt):
    client = anthropic.Anthropic(api_key=key)
    reply = client.messages.create(
        model="claude-opus-5", max_tokens=256,
        messages=[{"role": "user", "content": prompt}])
    return next(
        b.text for b in reply.content if b.type == "text")
```

Source: `CODEALONGS/day_1/m1_model_access/01_closed_model_call.py`

<!--
Read down the left edge, not across: client, call, return. Three vendors, one
shape. The differences are naming — `contents` / `input` / `messages` — and
one real design difference worth pausing on.

Claude returns a list of content blocks rather than a string, because a
response may contain thinking blocks before the text. `reply.content[0].text`
is the bug everyone writes first; picking the text block is the fix. That is
the first hint of something M2 makes central: a model call is structured, not
a string in and a string out.

The full file reads keys from .env and reports which providers are configured.
Keep the teaching path simple here: the point is the repeated call shape, not a
dispatch framework.
-->

---

# M1.2.3 · A proprietary model has more than chat

The same model family may support:

- text generation and structured extraction
- image, document, and chart understanding
- tool or function calling
- audio and grounded responses, where supported

In the code-along, change one variable at a time: ask for one sentence, then
three bullets, then a small JSON-shaped answer.

<!--
This is not a second snippet. It is guided exploration of the first one.
Availability varies by model and provider, so verify a feature before building
a dependency on it.
-->

---

# M1.3.1 · Local open weights keep inference on this machine

```python
os.environ.setdefault("HF_HUB_OFFLINE", "1")

generate = pipeline(
    "text-generation",
    model=str(MODELS / "smollm2-135m-instruct"),
)
reply = generate(
    "Name one risk in a portfolio with 52% in AAPL.",
    max_new_tokens=30,
)
print(reply[0]["generated_text"])
```

Source: `CODEALONGS/day_1/m1_model_access/03_local_model_call.py`

No key. No network. No per-call bill.

<!--
The weights are committed to this repository, so thirty people on venue wifi
download nothing. The file shows the `snapshot_download` call that put them
there — any Hub model id works the same way — but the line that runs points at
the local folder, and HF_HUB_OFFLINE makes a missing file fail loudly instead
of silently fetching.

The code-along then opens the model folder: config, tokenizer, shards,
prompt format, generation, decoding.
-->

---

# M1.3.2 · What a local model costs you

| You gain | You give up |
|---|---|
| No key, no network, no per-call bill | Capability — this model is 135M parameters |
| Data never leaves the machine | Someone must serve and update it |
| Stable, versioned behaviour | Hardware becomes your problem at scale |

Run it and read the answer honestly. A small local model is the right tool for
a narrow job, and the wrong tool for an open-ended one.

<!--
The cohort model is deliberately small, so it demonstrates the local boundary
rather than competing with a frontier model. Its weak output is teaching
material, not an accident — we use it again in M1.5 and it is the reason M2
and M3 exist.

Do not let the room conclude "local models are bad." The honest claim is that
capability is one axis among six, and this one is at the far end of it.
-->

---

# M1.4.1 · Proprietary and open-weight models are different trade-offs

| | Proprietary model | Open-weight model |
|---|---|---|
| Fastest first feature | Usually lower setup | Depends on hosting and setup |
| Capability | Often broad frontier capability | Strong and rapidly evolving |
| Cost | Usage pricing | Hosting or infrastructure cost |
| Data boundary | Provider or cloud agreement | Can run in a controlled boundary |
| Control | Provider roadmap | More model and deployment control |

> Neither is better. The feature, data boundary, cost, and operating model decide.

<!--
You have now run both, so this table is a recap rather than a preview. That
ordering is deliberate: a comparison of things nobody has seen is a list of
adjectives.

This is not an ideological closed-versus-open debate. A team may use both in
one application: a high-capability hosted model for uncertain work and an
owned local model for a narrow, high-volume task. The assistant in M1.5 does
exactly that, and falls back from one to the other.
-->

---

# M1.4.2 · Choose the smallest sufficient model and deployment

| Ask first | Why it matters |
|---|---|
| What is the task and modality? | Chat, speech, image, embeddings, classification |
| How good and fast must it be? | A draft and a compliance decision differ |
| What can it cost? | Calls, tokens, GPUs, and engineering effort |
| Where may data go? | Vendor, cloud account, provider, or local machine |
| What must the organisation control? | Weights, licence, deployment, behaviour |

> Start with the simplest option that is good enough for the real task.

<!--
Use scenarios instead of a list of fashionable model names: transcription
needs a speech specialist; semantic search needs embeddings; local-sensitive
work may favour a small local model. This is a decision framework, not a
benchmark debate.

Point back to the M1.A candidates here and ask two or three learners which row
decides their case.
-->

---

# M1.5.1 · Build the assistant: facts in, logged answer out

```python
def build_prompt(question, facts):
    given = "\n".join(f"{k}: {v}" for k, v in facts.items())
    return (
        f"{SYSTEM}\n\nFacts:\n{given}"
        f"\n\nQuestion: {question}"
    )

def answer(question, facts, call_model):
    prompt = build_prompt(question, facts)
    log.info("prompt_chars=%d", len(prompt))
    reply = call_model(prompt)
    log.info("reply_chars=%d", len(reply))
    return reply
```

Source: `CODEALONGS/day_1/m1_model_access/05_advisor_assistant.py`

<!--
This is the module's payoff and the first thing all day that is an
application rather than a call. Three moves: assemble instruction plus
grounding facts plus question, measure both sides of the boundary, and take
the model as a parameter so the caller decides which one.

`call_model` being injected is not style. It is what makes the boundary
testable without a key, and it is the same seam the lab and every later module
use.

The snippet uses the local SmolLM model so the application boundary is visible
without a provider key or network. The point is the boundary: facts in, model
call out, measured reply back.
-->

---

# M1.5.2 · Carry M0 practice into AI code

- configuration outside business logic — keys from `.env`, never source
- log the outcome, the model id, duration, and usage where available
- handle missing or empty output safely
- accept the model as a parameter, so tests never call a live provider

> First call proves access. This boundary makes access maintainable.

<!--
Every one of these is ordinary software engineering, which is the point:
almost nothing about an AI feature is new engineering. What is new is that the
dependency is non-deterministic, remote, metered, and occasionally wrong — so
the ordinary practices matter more, not less.

The empty-output case is the lab's job, and it is not hypothetical: a
truncated response, a safety refusal, and a quota error all reach your code as
"no usable text".
-->

---

<!-- _class: lead -->

# M1.L · Lab: AI assistant reference implementation

Start from the M1.5 assistant. Give it the two things it does not have yet.

**Mini lab** — one controlled instruction, one concise response.

**Main lab** — a terminal-first `reply(message, history)` application: carry
conversation history correctly, return a safe message when the model produces
no usable text, and prove both with two tests that never call a provider.

Optional extensions: a Gradio wrapper, then swap in the local model.

<!--
The snippet already did prompt assembly, configuration, and logging. The lab
adds exactly what it left out — memory across turns and the empty-response
path — so nobody rebuilds what they just read.

The lab deliberately avoids database and retrieval complexity; learners use
synthetic data embedded in code. A UI wraps an understood Python function; it
does not replace understanding it.

**Instructor only:** offer the hosted and local paths as comparisons, not as a
requirement that every learner complete both in the first pass.
-->

---

# M1.6.1 · Cloud platforms provide a governed model boundary

| Cloud platform | What it adds |
|---|---|
| Google Cloud / Vertex AI | Gemini access, project, IAM, billing |
| AWS / Bedrock | Model catalogue, AWS identity, governance controls |
| Azure AI | Model catalogue, Azure identity, enterprise controls |

Everything so far used a key in `.env`. In your organisation, it will not.

<!--
This is the section the room has been waiting for since M1.2. Cloud catalogues
change; the stable lesson is that a platform introduces a project or account,
identity and access management, billing, regional controls, and organisational
governance. It is not just another API URL.

Nobody here can run the next slide today, and that is fine — it needs a
project, an identity, and a role that someone else grants. Show it, name what
would have to be true, and move on.
-->

---

# M1.6.2 · The same Gemini capability through Vertex AI

```python
client = genai.Client(
    vertexai=True,
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location="global",
)
reply = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt,
)
```

Source: `CODEALONGS/day_1/m1_model_access/07_cloud_hosted_models.py`

Gemini through Vertex AI changes the **identity and governance boundary**, not
the business question.

<!--
Compare this to M1.2.2 line by line: the model, the prompt, and the returned
text are identical. What changed is who vouches for the caller — an API key
you hold, versus a project and an IAM-authenticated identity your organisation
grants and can revoke.

It is not Amazon Bedrock using Gemini; Bedrock is a separate cloud catalogue.
The same file also shows hosted open weights through an inference provider —
open weights someone else runs and scales — which is the fourth quadrant of
the same grid.
-->

---

# M1.7.1 · Access is only the first engineering problem

We asked the assistant how concentrated a portfolio was. It is 52% AAPL, and
the system prompt said *never invent a number*:

```text
INFO:advisor:backend=smollm2-135m-instruct
INFO:advisor:prompt_chars=267
Answer: 49.9%
```

Access was never the hard part.

> Next: why this happens, and how an engineer builds on top of it anyway.

<!--
Run this live if the timing allows; it reproduces. A small model, given the
right number in its own prompt and told not to invent one, invented one.

This is the whole rest of the course in one line. It is why M2 explains tokens
and context, why M3 asks which pattern the problem needs, why M4 grounds
answers in retrieved text, why M9 puts a human in front of client-facing
output, and why the capstone forbids a model from calculating anything.

Do not resolve it here. Leave the room slightly uncomfortable — the discomfort
is the motivation for the next four days.
-->
