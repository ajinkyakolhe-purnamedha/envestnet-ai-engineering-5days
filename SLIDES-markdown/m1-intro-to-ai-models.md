---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M1.0.1 · Introduction To AI Models

What they do, where to get them, what they cost

By the end of this module you can:

- Name the four ways to put a model in your application
- Call a closed model and an open model, in Python
- Argue capability vs cost vs **ownership** for a real feature
- Ship a working chatbot — online *and* fully offline

<!--
~75 minutes, with the last 30 hands-on.

Frame the module as a model-access decision. By the end, students should be
able to answer: which model, where does it run, where does the data go, and why
is that the right trade-off for this feature?
-->

---

# M1.1.1 · What Models Can Do Now

**Language**

- Write, rewrite, summarise, translate
- Extract structure from unstructured text
- Reason through multi-step problems
- Write and debug code

**Beyond language**

- See — images, screenshots, documents, charts
- Hear and speak — transcription, synthesis
- Generate — images, video, audio
- Act — call your tools, run your code

The engineering question:

```text
Can I make it reliable, affordable, and grounded in my data?
```

<!--
Demo slide. Do not read the bullets. Show two or three things live, using
whatever you have open. Suggestions that work well with engineers:

  - Paste a stack trace, ask for the root cause
  - Screenshot a UI, ask for implementation notes
  - Paste a chunk of the Chronos prices CSV, ask for the trend as JSON

Then use the question at the bottom as the transition. Capability is not the
end of the engineering problem. Reliability, cost, data boundary, evaluation,
and integration are the work.

Keep this to 10 minutes. It's very easy to burn half the module on demos.
-->

---

# M1.1.2 · A Model Is Not A Product

**What you just watched**

- A human pasting context into a box
- A human deciding what to ask
- A human judging whether the answer was any good
- A human carrying the result somewhere useful

Raw capability, with a person doing the integration by hand.

**What makes it a feature**

- It lives **where the work already happens**
- It gets its context **automatically**
- It fails safely, and visibly
- Someone measured whether it's good enough

Same model. The difference is entirely engineering.

Model capability becomes a product only after engineering wraps it.

<!--
This bridge stops the demo from becoming the lesson. The demo was manual:
someone chose the input, supplied context, judged the output, and moved the
answer somewhere useful. A product has to do those steps inside software.

Land the four right-hand rows as the actual work of the next five days:
  - "where the work happens" -> it's in the CRM, the IDE, the ticket queue.
    Nobody wants another chat window.
  - "context automatically" -> the model doesn't know your holdings, your
    customer, your codebase. Getting it there is M2 and M4.
  - "fails safely" -> it will be confidently wrong. M2 explains why, M3 covers
    guardrails and red-teaming.
  - "someone measured it" -> evals. M3. Without them you are guessing.

The core distinction is model versus product. A model is a capability. A
product is the model plus context, workflow, permissions, evaluation, safety,
UI, monitoring, and ownership.
-->

---

# M1.1.3 · The Application Gap

**Cloud — the mature market**

- Software built on the platform: **10×** the platform's own revenue
- The platform is big. What people **built on it** is ten times bigger.

**AI — today**

- Platforms earn **10×** what the software on them earns
- Exactly inverted. The application layer barely exists yet.

If AI follows the cloud pattern, more value moves to the application layer.

That application layer is built by engineers.

<!--
This is the commercial argument for building applications rather than only
studying models. Keep it as an order-of-magnitude framing, not a precise market
forecast.

CLOUD, mature: the platform layer (AWS, Azure, GCP selling compute and storage)
earns X. The software built on that platform earns roughly 10X. That is the
settled end-state of a platform shift — the platform enables far more value
than it captures.

AI, today: exactly the other way round. The model platforms are capturing
roughly 10x what the applications built on them earn. That is not a permanent
state, it is an early state — it is what cloud looked like before the SaaS wave
arrived.

If the ratio shifts toward applications, the work is product engineering:
workflow integration, data access, evaluation, security, UX, and operations.
Those are software-engineering problems around a model.

Have the source for the 10x figures available if this slide is delivered. The
numbers are useful as a shape, but they are not required for the technical
argument.

Two honest caveats worth pre-empting if challenged:
  1. "AI software revenue is early" is partly a measurement artifact — many AI
     features ship inside existing SaaS products and are never counted as AI
     revenue separately.
  2. Model-platform revenue is self-reported and inconsistently defined across
     labs, so treat it as an order of magnitude, not a precise figure.

Re-check the ratio before each delivery. This is the fastest-moving number in
the deck.
-->

---

# M1.2.1 · Four Ways To Use A Model

| | Where the weights live | Where it runs | You need |
|---|---|---|---|
| **1** | Vendor (closed) | Vendor's servers | API key |
| **2** | Vendor (closed) | Your cloud account | Cloud IAM |
| **3** | Open, downloaded | **Your machine** | Nothing |
| **4** | Open, hosted | Someone's GPUs | API key |

Same four questions every time: **capability**, **cost**, **where the data goes**, **who owns the result.**

<!--
This table is the spine of the module — the next four slides are one code
example each, in this order. Tell them that so the sequence reads as a tour.

The row that surprises people is 3: no key, no account, no network, no bill.
Many engineers have never run a model locally and assume it needs dedicated
infrastructure. The offline lab makes the local path concrete.

Rows 2 and 4 are the "grown-up" versions of 1 and 3 — same model, different
billing and data boundary. That's usually the real enterprise decision, and
it's a procurement conversation as much as a technical one.
-->

---

**Four Ways to Use a Model · 1 of 4**

# M1.2.2 · Closed Model, Vendor API

```python
"""Way 1: closed model, straight from the vendor."""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)      # reads GEMINI_API_KEY
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

NOTE = "Cash is 40% of the book, AAPL is 52%."

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=("Return exactly one sentence. "
              f"Name the biggest concentration risk: {NOTE}"),
    config={"max_output_tokens": 60},
)

print(response.text)
```

Full running version: `SLIDES-markdown/m1/first_call.py`

**What to notice**

- Two required fields here: `model` and `contents`
- The API is **stateless**
- No session, no connection; every call carries its input
- The key comes from the environment, never the code
- Fastest path to a working feature
- You rent capability; the model artifact is not yours

<!--
Statelessness is the concept to make precise. There is no durable conversation
on the model server. A chat request is the transcript sent again on each turn.
That is why context windows matter in M2, why long chats get expensive, and why
M9 treats memory as a transcript management problem.

max_tokens is a hard cap on the response, not a target. Set it too low and you
truncate mid-sentence — a very common first bug.

Never put a key in source. Use an environment variable, a secrets manager, or
cloud IAM. This rule applies to notebooks too.
-->

---

**Four Ways to Use a Model · 2 of 4**

# M1.2.3 · Closed Model, One Boundary

```python
"""Way 2: put the provider behind a small function."""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

def call_gemini(prompt: str) -> str:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
    )
    return response.text

print(call_gemini("Name one portfolio risk."))
```

Full running version: `SLIDES-markdown/m1/cloud_call.py`

**What to notice**

- Provider details live in one function
- Product code calls `call_gemini(...)`, not a scattered SDK
- The model ID is configuration, not business logic
- `gemini-2.5-flash-lite` is the cheap working demo model
- **Why this row exists:** swapping providers later should be configuration, not surgery.

<!--
This slide uses Gemini directly because that is the key available in the
workshop `.env`. The engineering point is still the same: keep provider details
at the boundary so later procurement or cloud decisions do not leak through the
application.

Caveat worth knowing: feature parity lags on partner platforms. Some newer API
features appear on the first-party API first. Check before promising one.
-->

---

**Four Ways to Use a Model · 3 of 4**

# M1.2.4 · Open Model, Your Machine

```python
"""Way 3: open model, on your laptop. No key, no network."""

from transformers import AutoModelForCausalLM, AutoTokenizer

PATH = "../OFFLINE-AI-Models/smollm2-135m-instruct"

tokenizer = AutoTokenizer.from_pretrained(
    PATH, local_files_only=True
)
model = AutoModelForCausalLM.from_pretrained(
    PATH, local_files_only=True
).eval()

messages = [
    {"role": "system", "content": "You explain portfolios."},
    {"role": "user", "content": "One holding is 52% of it."},
]

prompt = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
inputs = tokenizer(prompt, return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=60, do_sample=False)

new = out[0, inputs["input_ids"].shape[-1]:]
print(tokenizer.decode(new, skip_special_tokens=True))

# No API key. No per-token bill. No data leaving the box.
# This half-gigabyte is the thing you can fine-tune in M6.
```

Full running version: `SLIDES-markdown/m1/open_local.py`

**What to notice**

- No key. No account. No network after the download.
- ~260 MB on disk, runs on a laptop CPU
- Same `messages` shape you just learned
- The weights are local files
- Slower and less capable than row 1
- The artifact can be adapted, evaluated, and served under your control

<!--
Run this live if possible. The important observation is operational: after the
download, the model call does not need a network, an API key, or a per-token
bill.

Set expectations honestly: a 135M model is not going to impress anyone at
conversation. It will follow a narrow instruction reasonably well. That is the
correct use for small models — one job, done cheaply, a million times.

This file is what M6 can fine-tune. Fine-tuning does not make the model know
new changing facts; it changes behavior for a narrow task. That distinction is
handled explicitly in M6.

Practical: the workshop repo already carries the weights. If you swap to a
larger model, pre-download before the session or the room stalls on a progress
bar.
-->

---

**Four Ways to Use a Model · 4 of 4**

# M1.2.5 · Open Model, Hosted

```python
"""Way 4: open model, someone else's GPU."""

import os

from huggingface_hub import InferenceClient

client = InferenceClient(api_key=os.environ["HF_TOKEN"])

out = client.chat_completion(
    model="Qwen/Qwen3-235B-A22B-Instruct",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=512,
)

print(out.choices[0].message.content)

# Same weights as the laptop version -- rented compute.
# Move to your own GPUs later: this code doesn't change.
# You need a key here, but you don't need permission.
```

Full running version: `SLIDES-markdown/m1/open_hosted.py`

**What to notice**

- Open weights, industrial-scale hardware
- A key again — but for *compute*, not for the model
- Portable: move to your own GPUs, code unchanged
- Access to models far too big for a laptop
- Open-model portability without buying GPUs

<!--
This row is common in production open-model work. Large open models do not fit
on a laptop, but hosted inference lets a team rent GPU time while keeping
portability. If a provider changes price or reliability, the weights can be
served elsewhere.

Providers to name: HuggingFace Inference, Together, Fireworks, Groq, and
managed open-model catalogues. Don't pick a favourite from the front of the
room.

The distinction is compute versus capability. A hosted provider can revoke
access to its endpoint. It cannot remove the open weights from your architecture
if you have planned for portability.
-->

---

# M1.3.1 · What Changes In Production

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=PROMPT,
    config={"max_output_tokens": 80},
)

# 1. Log what it cost. Every call, every time.
usage = response.usage_metadata
print(f"usage prompt={usage.prompt_token_count} "
      f"output={usage.candidates_token_count}")

# 2. Check the response shape before reading text.
if response.text:
    print(response.text)
```

Full running version: `SLIDES-markdown/m1/production_call.py`

**What to notice**

1. **Load secrets from `.env`** — never paste keys into code
2. **Use Flash Lite for demos** — cheap enough to run live
3. **Log tokens** — every call, every time
4. **Check text exists** before treating the call as successful

The first model call proves access. This version handles production outcomes.

<!--
The habit worth teaching here is #3, and it generalizes past any one vendor:
a model call has more outcomes than "worked" and "threw an exception". It can
return a successful HTTP 200 and still not answer you — safety classifiers
decline, content gets truncated at max_tokens, a tool call comes back instead
of text. Code that reaches straight for content[0].text handles exactly one of
those and breaks on the rest.

The fallback parameter is the concrete instance: a declined request is re-run
server-side on another model in the same call, so a false-positive refusal
doesn't become a user-visible failure. Worth mentioning that benign work in
security and life-sciences adjacent domains is where false positives cluster.

Token logging is operational data. Without it, cost, latency, and regression
questions become guesswork.
-->

---

# M1.4.1 · The Models Worth Knowing

**Closed — general purpose**

| Model | Reach for it when |
|---|---|
| Gemini 2.5 Flash-Lite | cheapest live demos, routing, extraction |
| Gemini 2.5 Flash | stronger fast default |
| Gemini Pro tier | harder reasoning or multimodal work |
| GPT family | ecosystem and tool support |

**Open weights — general purpose**

| Family | From | Known for |
|---|---|---|
| Qwen | Alibaba | Breadth, strong small models |
| DeepSeek | DeepSeek | Reasoning, very low cost |
| Llama | Meta | Ecosystem, tooling |
| Kimi | Moonshot | Coding |
| GLM | Zhipu | Speed, long context |

These are generalists: one model, many jobs.

There is another shelf: specialist models.

<!--
Prices and rankings rot quickly. Re-check before delivery and treat the table
as a current example, not durable course truth.

Three framings that outlive the specific numbers:

1. THE PRICE SPREAD CAN BE ORDERS OF MAGNITUDE, not a small constant factor.
   On a feature doing millions of calls, that can decide whether the feature is
   operationally viable. This is why M2's model-routing discussion matters.

2. THE FRONTIER GAP HAS NARROWED but has not closed. Open models now match
   closed models on many benchmarks. On the hardest agentic and long-horizon
   work, closed frontier models are still ahead. Both halves of that sentence
   are true and people tend to only believe one.

3. "OPEN SOURCE" IS MOSTLY "OPEN WEIGHTS". You get the weights, not the
   training data or pipeline. That distinction matters legally and it matters
   when someone asks whether you can audit the model. Say it plainly.

Licences differ and it is not a footnote: Qwen and DeepSeek are typically
Apache-2.0, Llama has its own usage terms. If the pitch is "IP you own", legal
will read the licence.

Do not turn this into a benchmark debate. The durable lesson is the decision
axis: capability, latency, cost, data boundary, ownership, and serving
complexity.
-->

---

# M1.4.2 · One Job, Done Better

| Job | Open models to look at | Replaces |
|---|---|---|
| **Images** | Flux · Qwen-Image · Stable Diffusion | A stock photo budget |
| **Video** | Wan 2.2 · HunyuanVideo · LTX-2 | A production shoot |
| **Speech → text** | Whisper | A transcription service |
| **Text → speech** | Kokoro · XTTS | A voice-over artist |
| **Meaning vectors** | arctic-embed · bge | *This one powers M4* |
| **Re-ranking** | bge-reranker | Better search results |

A single-purpose model can beat a large general model at one job, while being
smaller, faster, and cheaper.

<!--
Model names change quickly. Re-check examples before delivery. The stable
concept is specialist versus generalist.

The engineering mistake is reaching for the largest general model for every
task. That is expensive and often less accurate than a specialist.

Why the specialist wins, three reasons and they compound:
  1. Better at the job. All of its parameters learned one thing.
  2. Smaller and faster. Whisper transcribes on a laptop in real time; asking a
     frontier multimodal model to do it costs more and takes longer.
  3. Cheaper, by an order of magnitude or more, on high-volume work.

The judgement call to teach: use a generalist when the task is open-ended or
you don't yet know the shape of the problem. Use a specialist the moment the
job is well-defined and the volume is real. Most production systems end up as
a handful of specialists with one generalist for the messy parts.

If discussing emerging categories such as world models, keep it brief. They are
not required for this workshop's application path.

Two callbacks that matter:
  - arctic-embed is the 85 MB model they downloaded in M0. It is a
    single-purpose model, and they already own one.
  - Re-ranking will come back in M5 as an advanced RAG pattern.
-->

---

# M1.4.3 · Closed vs Open: The Real Decision

| | Closed | Open |
|---|---|---|
| **Capability** | Frontier, especially on hard agentic work | Close, and closing |
| **Cost** | $$ per token, forever | Cents per token, or your own hardware |
| **Time to first feature** | Minutes | Hours to days |
| **Your data** | Leaves your boundary | Never has to |
| **Ownership** | You rent capability | **You own the artifact** |
| **Lock-in** | Vendor's roadmap and pricing | Yours |

Pragmatic path:

```text
start closed to test value
move open when cost, ownership, or data boundary matters
```

<!--
The pragmatic path saves time. Prototype on a strong closed model when the
feature is still uncertain. That tells the team whether the workflow has value
before they spend time on serving infrastructure.

Then measure: cost per call, latency, data boundary, and whether the model
behavior needs to become owned IP. If one of those hurts, the team can move
open with a known task and acceptance criteria.

The anti-pattern is choosing closed or open as an identity before the feature is
understood. Both directions can waste time if chosen too early.

Ownership is the row that matters most for this audience, and it's the M0
argument arriving on schedule: anyone can call the same API you're calling.
Nobody else has your data.
-->

---

<!-- _class: lead -->

# M1.L1 · Lab

Your first AI chatbot — two ways

<!--
Laptops out. Two paths, and everyone should do both if time allows: A proves
the hosted path works, B proves they don't need it.

Circulate for the first five minutes — key setup is where people get stuck, and
they won't say so.
-->

---

# M1.L2 · Lab: A Working Chatbot

```python
def reply(message, history):
    msgs = [
        {"role": m["role"], "content": m["content"]}
        for m in history
    ]
    msgs.append({"role": "user", "content": message})

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"{SYSTEM}\n\nUser: {message}",
    )
    return response.text
```

Full running version: `SLIDES-markdown/m1/gradio_chat.py`

**What to notice**

- Gradio hands you `history` — you convert it to `messages`
- `return` sends the model text back into the UI
- The system prompt is where the *product* lives
- About 25 lines to a shareable web app

1. Run it → then **change the system prompt** and watch the personality change.

Done when: A browser chat window that streams a reply, with a system prompt you wrote yourself.

<!--
Gradio is a fast path from a Python function to a shareable UI. It is not the
production frontend pattern for Chronos, but it is useful for a first model
call because it removes unrelated frontend work.

The exercise that teaches the most is the system-prompt edit. Have students make
the assistant refuse to discuss anything but their portfolio, then try to talk
it out of that. The lesson is prompt control and prompt injection, not Gradio.

Common stumbles: forgetting `type="messages"` (Gradio's older tuple format has
a different shape), and yielding the delta instead of the accumulated string
(you get one character at a time in the UI).
-->

---

# M1.L3 · Lab: Pull The Network Cable

```python
def reply(message, history):
    msgs = [{"role": "system", "content": SYSTEM}]
    msgs += [
        {"role": m["role"], "content": m["content"]}
        for m in history
    ]
    msgs.append({"role": "user", "content": message})

    out = chat(msgs, max_new_tokens=256)
    return out[0]["generated_text"][-1]["content"]
```

Full running version: `SLIDES-markdown/m1/gradio_offline.py`

**What to notice**

- `HF_HUB_OFFLINE=1` — this is a proof, not a config
- Weights come from a folder in the repo
- No key, no network, no bill, no data leaving the box
- Same Gradio wrapper as Lab A

1. Run it, then **turn off your wifi and run it again.** Note where quality drops off vs Lab A. That gap is what the rest of the week reduces.

Done when: A chatbot answering with the network disabled.

<!--
The wifi-off step is the point. Do it at the front of the room too.

PREP REQUIRED — see offline_models.md for the vetted models and the sharding
recipe. Weights ship in the workshop repo, under GitHub's 100 MB per-file
limit, so participants clone rather than download on venue wifi. Pre-stage this;
do not have thirty people hit HuggingFace simultaneously.

One honest discrepancy to resolve before delivery: the outline budgets ~500 MB
for the generative model, but the smallest decent instruct model
(Qwen2.5-0.5B-Instruct) is ~1 GB in fp16. Either accept ~1 GB, or ship a
quantised build to hit 500 MB. The 85 MB arctic-embed-xs embedding model is
comfortably within budget either way and is what M4's offline RAG uses.

Expect the quality gap to be clear. Use it as a diagnostic question: what would
make the small model good enough for one specific job? Answers: narrower task,
better prompt, retrieved context, fine-tuning, or a different model tier. Those
map to M2, M3, M4, and M6.

Alternative labs if a group finishes early or wants something else: Gradio live
transcriber, text-to-image, or trend summaries over the Chronos prices CSV
from M0.
-->

---

<!-- _class: lead -->

# M1.5.1 · Where That Leaves Us

You can now call a model — four different ways — and you have a working chatbot.

You have also seen it be **wrong, slow, and forgetful**.

Next: **why**, and what you can do about it.

<!--
Close by naming the failures they just watched, because they will have hit all
three in the lab: wrong (small model hallucinates), slow (streaming exists for
a reason), forgetful (nothing persists between runs).

Those three complaints map exactly onto M2: model choice and size explain
wrong, cost and latency explain slow, and the context window explains
forgetful. Say that — it makes M2 feel like the answer to a question they now
have rather than the next set of slides.
-->
