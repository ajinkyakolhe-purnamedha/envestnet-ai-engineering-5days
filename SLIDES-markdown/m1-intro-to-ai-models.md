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
- Call a proprietary, cloud-hosted, open-weight, and local model
- Choose a model and deployment boundary for a feature
- Build a small, maintainable AI assistant for a real workflow

<!--
This module is the bridge from M0 Python to the rest of AI engineering. The
throughline is a synthetic portfolio assistant: one shared implementation
example, not the scope of the course. The model is impressive, but the
application is what makes it useful in any workflow.

**Instructor only:** reserve roughly half the module for Section 2 and the
hands-on work. Capability demonstrations should be short and purposeful.
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
An AI application must make that answer useful, safe, and affordable.
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
| Specialist models | Speech, image, embedding, reranking | Often better for one narrow task |

Model names change quickly. The engineering skill is recognising the category
and choosing it for the task.

<!--
These are dated examples, not a leaderboard. Explain that open weights do not
automatically mean open training data or an unrestricted licence.
-->

---

# M1.1.4 · A model is not a product

| Manual model use | Product feature |
|---|---|
| A person pastes data into chat | The application receives permitted workflow data |
| A person writes the prompt | Code supplies instructions consistently |
| A person decides whether to trust it | The application evaluates and shows limits |
| A person copies the result elsewhere | The result appears in the workflow itself |

> A product is model + data + workflow + safety + evaluation + operations.

<!--
The same model can be used manually or embedded in an application. The
difference is engineering. This is the course map: later modules add context,
evaluation, retrieval, adaptation, tools, and operations around this boundary.
-->

---

# M1.1.5 · Every platform creates an application wave

```text
Computers created software companies.
The internet created web applications.
Cloud created SaaS applications.

AI creates a new application layer.
```

Platforms provide a general capability. Applications make that capability
specific, useful, and valuable for a user and workflow.

<!--
Use one of the supplied historical-platform visuals here. The durable lesson
does not depend on a specific market-revenue ratio: as infrastructure becomes
available, builders create applications that solve previously uneconomic or
impossible problems.
-->

---

# M1.1.6 · Models are infrastructure, not the finish line

A model does not know:

- your customers, cases, policies, documents, or internal systems
- which data it is allowed to use
- what the user is trying to complete
- what a correct answer means for your organisation

> The opportunity is to design an AI-native workflow around the model.

<!--
Use the second supplied visual here. A model is a general capability; the
application supplies context, permissions, workflow, judgement, and user
experience.
-->

---

# M1.1.7 · Many AI applications still need to be imagined and built

Every repeated **question, decision, document, conversation, review, search,
and workflow** is a candidate for an AI application.

- Advisor copilot for a portfolio review
- Support assistant for triaging and drafting a response to an exception
- Policy-document assistant for extracting constraints
- Operations assistant for reviewing an incoming case or hand-off

> The model may be shared by everyone. The application is what you build.

<!--
Use the strongest of the supplied visuals here. The point is possibility, not
that every workflow should be automated. The next question is practical: how
do we access a model from an application?
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

# M1.2.1 · Four practical paths to a model

| Path | Example | What changes |
|---|---|---|
| Proprietary, direct | Gemini API | Fastest path from Python to a model |
| Proprietary, cloud | Gemini through Vertex AI | Project, IAM, billing, organisation boundary |
| Open weights, hosted | Hosted inference provider | Model choice without owning GPUs |
| Open weights, local | SmolLM2 on this laptop | No key, no network, no per-call bill |

Ask the same questions every time: **task, quality, cost, data boundary,
ownership, and serving effort.**

<!--
Use “open weights” precisely: weights may be available while training data,
training pipeline, and licence terms remain different. The direct API and
Vertex examples deliberately use the same Gemini capability; the boundary,
identity, and governance are what change.
-->

---

# M1.2.2 · Cloud platforms provide a governed model boundary

| Cloud platform | What it adds |
|---|---|
| Google Cloud / Vertex AI | Gemini access, project, IAM, billing |
| AWS / Bedrock | Model catalogue, AWS identity, governance controls |
| Azure AI | Model catalogue, Azure identity, enterprise controls |

We use **Gemini through Vertex AI** next because the same model makes the
difference between API-key and cloud-identity access easy to see.

<!--
Cloud catalogues change. The stable lesson is that a platform introduces a
project/account, identity and access management, billing, regional controls,
and organisational governance. It is not just another API URL.
-->

---

# M1.2.3 · Proprietary model: one direct Gemini call

```python
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="Name one risk in a portfolio with 52% in AAPL.",
)
print(response.text)
```

Source: `CODEALONGS/day_1/m1_model_access/01_gemini_text.py`

**Notice:** prompt in, response out; the key comes from `.env`, never source.

<!--
The full source includes dotenv setup and a safe “key not set” message. This
visible code intentionally teaches only one thing: calling a model.
-->

---

# M1.2.4 · A proprietary model has more than chat

The same model family may support:

- text generation and structured extraction
- image, document, and chart understanding
- tool or function calling
- audio and grounded responses, where supported

In the code-along, change one variable at a time: ask for one sentence, then
three bullets, then a small JSON-shaped answer.

<!--
This is not a second cookbook snippet. It is guided exploration of the first
one. Availability varies by model and provider, so verify a feature before
building a dependency on it.
-->

---

# M1.2.5 · The same Gemini capability through Vertex AI

```python
client = genai.Client(
    vertexai=True,
    project=project,
    location="global",
)
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="Name one risk in a portfolio with 52% in AAPL.",
)
```

Source: `CODEALONGS/day_1/m1_model_access/03_vertex_gemini.py`

Gemini through Vertex AI changes the **identity and governance boundary**, not
the business question.

<!--
Vertex uses a Google Cloud project and IAM-authenticated identity. This is the
enterprise access pattern to contrast with a direct API key. It is not Amazon
Bedrock using Gemini; Bedrock is a separate cloud catalogue.
-->

---

# M1.2.6 · Hosted open weights give access to a large ecosystem

```python
client = InferenceClient(api_key=token)
response = client.chat_completion(
    model="Qwen/Qwen3-32B",
    messages=[{"role": "user", "content": "Name one portfolio risk."}],
)
print(response.choices[0].message.content)
```

Source: `CODEALONGS/day_1/m1_model_access/05_hosted_open_model.py`

Open weights can reduce model lock-in. Hosted inference still has a provider,
account, data boundary, and operating cost.

<!--
The model name is an example, not a recommendation that should outlive this
delivery. Use a current provider/model that is available to the cohort.
-->

---

# M1.2.7 · Open-weight models can be specialists

| Job | Example capability |
|---|---|
| Speech → text | Transcribe a spoken portfolio update |
| Text → image | Generate a future wealth-dashboard concept |
| Embeddings | Represent meaning as numbers for search |
| Re-ranking | Put the most relevant results first |

> A specialist can be smaller, faster, cheaper, and better than a general
> model for one well-defined job.

<!--
**Instructor only:** prepare one speech-to-text and one text-to-image Hugging
Face demonstration. They are demonstrations, not required learner setup:
hosted model availability, quotas, and authentication change frequently.
-->

---

# M1.2.8 · Local open weights keep inference on this machine

```python
generate = pipeline(
    "text-generation", model=str(MODEL_PATH), local_files_only=True
)
reply = generate("Name one risk in a portfolio with 52% in AAPL.")
print(reply[0]["generated_text"])
```

Source: `CODEALONGS/day_1/m1_model_access/07_local_model.py`

No key. No network after the files are present. No per-call bill.

<!--
The cohort model is deliberately small, so it is useful for showing the local
boundary rather than competing with a frontier model. The code-along then
reveals the model folder, tokenizer, prompt format, generation, and decoding.
-->

---

# M1.3.1 · Proprietary and open-weight models are different trade-offs

| | Proprietary model | Open-weight model |
|---|---|---|
| Fastest first feature | Usually lower setup | Depends on hosting and setup |
| Capability | Often broad frontier capability | Strong and rapidly evolving |
| Cost | Usage pricing | Hosting or infrastructure cost |
| Data boundary | Provider or cloud agreement | Can run in a controlled boundary |
| Control | Provider roadmap | More model and deployment control |

> Neither is better. The feature, data boundary, cost, and operating model decide.

<!--
This is deliberately not an ideological closed-versus-open debate. A team may
use both in one application: a high-capability hosted model for uncertain work
and an owned local model for a narrow, high-volume task.
-->

---

# M1.3.2 · Choose the smallest sufficient model and deployment

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
-->

---

# M1.4.1 · Put the model behind a maintainable application boundary

```python
def reply_to_advisor(message, call_model):
    reply = call_model(message)
    logger.info("model_reply_received=%s", bool(reply))
    return reply or "I could not produce an answer. Please try again."
```

Source: `CODEALONGS/day_1/m1_model_access/09_model_boundary.py`

Carry M0 practices into AI code:

- configuration outside business logic
- logging of outcome, model ID, duration, and usage where available
- safe handling of missing output
- tests that do not call a live provider

<!--
First call proves access. This boundary makes access maintainable. The
code-along replaces the small lambda with a provider call, logs useful
operational data, and tests an empty response locally.
-->

---

<!-- _class: lead -->

# M1.L · Lab: AI assistant reference implementation

Build a small, maintainable assistant for a real workflow. We use the Chronos
Portfolio Assistant and synthetic portfolio facts as the shared reference
implementation.

**Mini lab** — Gemini call, one controlled instruction, one concise response.

**Main lab** — terminal-first `reply(message, history)` application with
dotenv configuration, correct history, logging, and two tests. The same shape
could support a service copilot, document assistant, or operations workflow.

Optional extensions: a Gradio wrapper, then a local-model implementation.

<!--
The lab deliberately avoids database and retrieval complexity; learners use
synthetic data embedded in code. A UI wraps an understood Python function—it
does not replace understanding it.

**Instructor only:** offer the hosted and local paths as comparisons, not as a
requirement that every learner complete both in the first pass.
-->

---

# M1.5.1 · Access is only the first engineering problem

You can now call a model through several boundaries.

You have also seen that models can be:

- wrong or insufficiently precise
- slow or expensive for a workload
- unaware of current private data
- convincing even when they should not be trusted

> Next: why these limits exist, and how an engineer works with them.

<!--
This closes the opening: the application opportunity is enormous, but model
access alone is not enough. M2 explains the underlying capability, context,
latency, and cost trade-offs that learners have just encountered.
-->
