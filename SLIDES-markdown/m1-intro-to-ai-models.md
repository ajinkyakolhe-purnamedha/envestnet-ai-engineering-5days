---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M1 · Introduction to AI Models

What they do, where to get them, what they cost

By the end of this module you can:

- Name the four ways to put a model in your application
- Call a closed model and an open model, in Python
- Argue capability vs cost vs **ownership** for a real feature
- Ship a working chatbot — online *and* fully offline

<!--
~75 minutes, with the last 30 hands-on.

Frame the module as a shopping trip, not a lecture. By the end they should be
able to answer "which model, from where, and why" for a feature — that question
is the whole job, and everything after M1 assumes they can answer it.
-->

---

# What Models Can Do Now

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

> The interesting question stopped being *"can it do this?"* and became
> **"can I make it do this reliably, cheaply, on my data?"**

<!--
DEMO SLIDE — do not read the bullets. Show two or three things live, using
whatever you have open. Suggestions that land well with engineers:

  - Paste a stack trace, ask for the root cause
  - Screenshot a UI, ask for the HTML/CSS
  - Paste a chunk of the Chronos prices CSV, ask for the trend as JSON

Then land the pivot at the bottom. That sentence is the thesis of the entire
five days: capability is table stakes now; reliability, cost, and data
ownership are the engineering. Everything from M2 onward is one of those three.

Keep this to 10 minutes. It's very easy to burn half the module on demos.
-->

---

# A Model Is Not a Product

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

> GPT is a model. ChatGPT is a product. **The distance between those two words is the job.**

<!--
The bridge slide, and it stops the demo becoming "AI is amazing, the end".

The move to make: the demo they just watched was impressive AND it was entirely
manual. You chose the input, you pasted the context, you read the output, you
decided if it was right, and then you did something with it. Strip the human out
and nothing happens. That is a capability, not a feature.

Land the four right-hand rows as the actual work of the next five days:
  - "where the work happens" -> it's in the CRM, the IDE, the ticket queue.
    Nobody wants another chat window.
  - "context automatically" -> the model doesn't know your holdings, your
    customer, your codebase. Getting it there is M2 and M4.
  - "fails safely" -> it will be confidently wrong. M2 explains why, M3 covers
    guardrails and red-teaming.
  - "someone measured it" -> evals. M3. Without them you are guessing.

The GPT/ChatGPT line is the one to land. Same weights underneath; one is a
research artifact and the other is a product used by hundreds of millions,
and the entire difference is the software wrapped around it.

Then straight into the next slide: that difference is also where the money is.
-->

---

# The Gap We're Here to Fill

**Cloud — the mature market**

- Software built on the platform: **10×** the platform's own revenue
- The platform is big. What people **built on it** is ten times bigger.

**AI — today**

- Platforms earn **10×** what the software on them earns
- Exactly inverted. The application layer barely exists yet.

When AI follows cloud, that ratio flips — and **a 100× swing** lands on the software side. **That gap is the job description.**

<!--
This is the commercial argument for the whole week, and it works because it is
one shape shown twice, inverted.

CLOUD, mature: the platform layer (AWS, Azure, GCP selling compute and storage)
earns X. The software built on that platform earns roughly 10X. That is the
settled end-state of a platform shift — the platform enables far more value
than it captures.

AI, today: exactly the other way round. The model platforms are capturing
roughly 10x what the applications built on them earn. That is not a permanent
state, it is an early state — it is what cloud looked like before the SaaS wave
arrived.

Then the punchline: when AI follows the same path, the ratio inverts. That is a
100x swing in where the revenue sits, and it lands on the application layer —
which is built by engineers writing features, not by researchers training
models. That is the room's opportunity, and it is why the next five days are
about building rather than about model architecture.

The 10x figures are Ajinkya's datapoint — have the source to hand, because a
sharp room will ask, and the number is doing a lot of work here.

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

# Four Ways to Use a Model

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
Most engineers have never actually run a model locally and assume it needs a
datacentre. Twenty minutes from now they'll have done it.

Rows 2 and 4 are the "grown-up" versions of 1 and 3 — same model, different
billing and data boundary. That's usually the real enterprise decision, and
it's a procurement conversation as much as a technical one.
-->

---

**Four Ways to Use a Model · 1/4**

# Closed Model, Vendor API

```python
"""Way 1: closed model, straight from the vendor."""

from anthropic import Anthropic

client = Anthropic()      # reads ANTHROPIC_API_KEY

NOTE = "Cash is 40% of the book, one holding is 52%."

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=16000,
    messages=[
        {"role": "user", "content": f"Name the risk: {NOTE}"},
    ],
)

print(response.content[0].text)
```

**What to notice**

- Three required fields: `model`, `max_tokens`, `messages`
- `messages` is a list of turns — the API is **stateless**
- No session, no connection; every call carries its whole history
- The key comes from the environment, never the code
- Fastest path to a working feature. You rent capability; you own nothing.

<!--
Statelessness is the concept that trips up most newcomers, and it's worth 60
seconds: there is no conversation on the server. A "chat" is you resending the
entire transcript every single turn. That's why context windows matter (M2),
why long conversations get expensive, and why caching exists.

max_tokens is a hard cap on the response, not a target. Set it too low and you
truncate mid-sentence — a very common first bug.

Never put a key in source. Environment variable, secrets manager, or your
cloud's IAM. Say it once, firmly; someone in the room is about to do it.
-->

---

**Four Ways to Use a Model · 2/4**

# Closed Model, Your Cloud

```python
"""Way 2: closed model, via your own cloud account."""

from anthropic import AnthropicBedrockMantle

# Auth is AWS IAM. Billing lands on your AWS bill.
# Traffic stays inside your account boundary.
client = AnthropicBedrockMantle(aws_region="us-east-1")

response = client.messages.create(
    model="anthropic.claude-opus-5",   # note the prefix
    max_tokens=16000,
    messages=[{"role": "user", "content": "Hello"}],
)

print(response.content[0].text)

# Same SDK, same request shape as the vendor API.
# What changes: who bills you, and where the data goes.
```

**What to notice**

- Different client, **identical** request shape
- Auth is your cloud's IAM, not a vendor key
- Billing lands on a bill you already have
- Model ID picks up a provider prefix
- **Why this row exists:** procurement, data residency, and an existing cloud commitment. Often the only option that clears review.

<!--
DRAFT — the outline had this as a TODO. I've assumed AWS Bedrock; swap the
client if Envestnet standardises on Azure/Foundry or GCP/Vertex. The three
client classes are AnthropicBedrockMantle, AnthropicFoundry, AnthropicVertex —
the rest of the code is unchanged, which is exactly the point of the slide.

The engineering point is small: same SDK, one line different. The point that
actually matters to this audience is organisational — going through the cloud
account means no new vendor contract, no new data-processing agreement, and
traffic that stays inside a boundary the security team already signed off on.
For a regulated business that is frequently the whole decision.

Caveat worth knowing: feature parity lags on partner platforms. Some newer API
features land on the first-party API first. Check before promising one.
-->

---

**Four Ways to Use a Model · 3/4**

# Open Model, Your Machine

```python
"""Way 3: open model, on your laptop. No key, no network."""

from transformers import pipeline

# Downloads once (~1 GB), then runs entirely offline.
chat = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct",
)

messages = [
    {"role": "system", "content": "You explain portfolios."},
    {"role": "user", "content": "One holding is 52% of it."},
]

out = chat(messages, max_new_tokens=64)
print(out[0]["generated_text"][-1]["content"])

# No API key. No per-token bill. No data leaving the box.
# This half-gigabyte is the thing you can fine-tune in M6.
```

**What to notice**

- No key. No account. No network after the download.
- ~1 GB on disk, runs on a laptop CPU
- Same `messages` shape you just learned
- The weights are now **a file you own**
- Slower and less capable than row 1 — and it is the only row where the result can become *your* IP.

<!--
Run this live if you possibly can. The moment a model answers on a laptop with
the wifi off is the moment M0's "customisable IP" argument stops being a slide
and becomes a thing they watched happen.

Set expectations honestly: a 0.5B model is not going to impress anyone at
conversation. It will follow a narrow instruction reasonably well. That is the
correct use for small models — one job, done cheaply, a million times.

The callback to land: this file is what M6 fine-tunes. Right now it's a generic
half-gigabyte; after fine-tuning on data only you have, it does something no
competitor can buy.

Practical: first run downloads the weights, so pre-download before the session
or the room stalls on a progress bar.
-->

---

**Four Ways to Use a Model · 4/4**

# Open Model, Hosted

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

**What to notice**

- Open weights, industrial-scale hardware
- A key again — but for *compute*, not for the model
- Portable: move to your own GPUs, code unchanged
- Access to models far too big for a laptop
- The pragmatic middle: open-model economics and ownership, without buying GPUs.

<!--
This row is how most serious open-model work actually ships. A 400B-parameter
open model is not running on anyone's laptop, but you can rent it by the token,
and — critically — you are not locked in. If the price moves or the provider
folds, the weights are still on HuggingFace and the same code points somewhere
else. That optionality is the difference between renting compute and renting
capability.

Providers to name: HuggingFace Inference, Together, Fireworks, Groq, plus the
open-model catalogues inside Bedrock and Vertex. Don't pick a favourite from
the front of the room.

The line to leave them with: "you need a key here, but you don't need
permission." Nobody can revoke your access to an open model — only to one
particular vendor's copy of it.
-->

---

# What Changes When It's Real

```python
with client.beta.messages.stream(          # 1. stream
    model="claude-opus-5",
    max_tokens=64000,
    betas=["server-side-fallback-2026-07-01"],
    fallbacks="default",                   # 2. auto-fallback
    messages=[{"role": "user", "content": PROMPT}],
) as stream:
    response = stream.get_final_message()

# 3. The model can decline. Check BEFORE reading content
#    -- on a refusal, response.content may be empty.
if response.stop_reason == "refusal":
    log.warning("declined: %s", response.stop_details)
else:
    print(response.content[0].text)

# 4. Log what it cost. Every call, every time.
log.info(
    "in=%d out=%d",
    response.usage.input_tokens,
    response.usage.output_tokens,
)
```

**What to notice**

1. **Stream** — long answers hit HTTP timeouts otherwise
2. **Fallback** — a declined request re-runs on another model automatically
3. **Check `stop_reason`** *before* reading content
4. **Log tokens** — every call, every time

Slide 1 was the demo. This is the version that survives a Monday morning.

<!--
The habit worth teaching here is #3, and it generalises past any one vendor:
a model call has more outcomes than "worked" and "threw an exception". It can
return a successful HTTP 200 and still not answer you — safety classifiers
decline, content gets truncated at max_tokens, a tool call comes back instead
of text. Code that reaches straight for content[0].text handles exactly one of
those and breaks on the rest.

The fallback parameter is the concrete instance: a declined request is re-run
server-side on another model in the same call, so a false-positive refusal
doesn't become a user-visible failure. Worth mentioning that benign work in
security and life-sciences adjacent domains is where false positives cluster.

Token logging pays for itself in week one. Without it, "why did the AI bill
triple?" is unanswerable — and it always gets asked.
-->

---

# The Models Worth Knowing

**Closed — general purpose**

| Model | In / Out per 1M |
|---|---|
| Claude Opus 5 | $5 / $25 |
| Claude Sonnet 5 | $3 / $15 |
| Claude Haiku 4.5 | $1 / $5 |
| GPT-5.5 | $5 / $30 |
| Gemini 3.1 Pro | $2 / $12 |

**Open weights — general purpose**

| Family | From | Known for |
|---|---|---|
| Qwen | Alibaba | Breadth, strong small models |
| DeepSeek | DeepSeek | Reasoning, very low cost |
| Llama | Meta | Ecosystem, tooling |
| Kimi | Moonshot | Coding |
| GLM | Zhipu | Speed, long context |

These are the **generalists** — one model, many jobs. There is another shelf entirely.

<!--
DRAFT — prices and rankings are from August 2026 and rot within weeks. Re-check
before every delivery; treat the table as a shape, not as truth.

Three framings that outlive the specific numbers:

1. THE PRICE SPREAD IS ~100x, not 2x. Frontier closed models run $5-30 per
   million output tokens; capable open models run cents. On a feature doing
   millions of calls that is the difference between a product and a science
   project. It's also why M2's model-routing discussion matters.

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

Don't turn this into a benchmark debate. Point at the leaderboards, move on.
-->

---

# One Job, Done Better

| Job | Open models to look at | Replaces |
|---|---|---|
| **Images** | Flux · Qwen-Image · Stable Diffusion | A stock photo budget |
| **Video** | Wan 2.2 · HunyuanVideo · LTX-2 | A production shoot |
| **Speech → text** | Whisper | A transcription service |
| **Text → speech** | Kokoro · XTTS | A voice-over artist |
| **Meaning vectors** | arctic-embed · bge | *This one powers M4* |
| **Re-ranking** | bge-reranker | Better search results |

> A single-purpose model beats a big general model **at that one purpose** — and it is smaller, faster and cheaper to run.

<!--
DRAFT — model names are August 2026 and rot fast. Re-check, and open two or
three on their sites live rather than reading the table aloud; these are much
more convincing seen than described.

The point of the slide, and say it directly: your instinct will be to reach for
the biggest general model for everything, because that is what the demos show.
That instinct is expensive and often just worse.

Why the specialist wins, three reasons and they compound:
  1. Better at the job. All of its parameters learned one thing.
  2. Smaller and faster. Whisper transcribes on a laptop in real time; asking a
     frontier multimodal model to do it costs more and takes longer.
  3. Cheaper, by an order of magnitude or more, on high-volume work.

The judgement call to teach: use a generalist when the task is open-ended or
you don't yet know the shape of the problem. Use a specialist the moment the
job is well-defined and the volume is real. Most production systems end up as
a handful of specialists with one generalist for the messy parts.

WORLD MODELS are the emerging fifth category — models that generate navigable
environments rather than flat video. Worth a sentence as "watch this space";
the open ones are not yet something you would build on.

Two callbacks that matter:
  - arctic-embed is the 85 MB model they downloaded in M0. It is a
    single-purpose model, and they already own one.
  - Re-ranking will come back in M5 as an advanced RAG pattern.
-->

---

# Closed vs Open: The Real Decision

| | Closed | Open |
|---|---|---|
| **Capability** | Frontier, especially on hard agentic work | Close, and closing |
| **Cost** | $$ per token, forever | Cents per token, or your own hardware |
| **Time to first feature** | Minutes | Hours to days |
| **Your data** | Leaves your boundary | Never has to |
| **Ownership** | You rent capability | **You own the artifact** |
| **Lock-in** | Vendor's roadmap and pricing | Yours |

> Not a religious question. **Start closed to find out whether the feature is worth building. Move open when ownership, cost, or data boundary starts to matter.**

<!--
This is the slide people will screenshot. Land the closing line properly.

The pragmatic path, and say it explicitly because it saves them months:
prototype on a closed frontier model, because you want to learn whether the
feature works at all before you spend a week on infrastructure. Then look at
your three numbers — cost per call at real volume, where the data is going, and
how much of the result you want to own. If none of them hurt, stay. If one
does, you already know exactly what the feature needs to do, which makes moving
to an open model a well-specified engineering task instead of a research
project.

The anti-pattern is picking a side first, on principle, and then discovering
six weeks in that the feature was never viable. Both religions cost the same.

Ownership is the row that matters most for this audience, and it's the M0
argument arriving on schedule: anyone can call the same API you're calling.
Nobody else has your data.
-->

---

<!-- _class: lead -->

# Lab

Your first AI chatbot — two ways

<!--
Laptops out. Two paths, and everyone should do both if time allows: A proves
the hosted path works, B proves they don't need it.

Circulate for the first five minutes — key setup is where people get stuck, and
they won't say so.
-->

---

# 🧪 Lab: A working chatbot (15 min)

```python
def reply(message, history):
    msgs = [
        {"role": m["role"], "content": m["content"]}
        for m in history
    ]
    msgs.append({"role": "user", "content": message})

    with client.messages.stream(
        model="claude-opus-5",
        max_tokens=4096,
        system=SYSTEM,
        messages=msgs,
    ) as stream:
        partial = ""
        for text in stream.text_stream:
            partial += text
            yield partial       # Gradio renders each yield
```

**What to notice**

- Gradio hands you `history` — you convert it to `messages`
- `yield` instead of `return` → text streams into the UI
- The system prompt is where the *product* lives
- ~25 lines to a shareable web app

1. `uv add gradio anthropic` → run it → then **change the system prompt** and watch the personality change.

Done when: A browser chat window that streams a reply, with a system prompt you wrote yourself.

<!--
Gradio is the fastest path from a Python function to a shareable UI. It is not
a production frontend and nobody should ship it, but for a workshop and for
internal demos it removes an entire day of frontend work.

The exercise that teaches the most is the system-prompt edit. Have them make
the assistant refuse to discuss anything but their portfolio, then try to talk
it out of that. Two minutes of that does more for their intuition about prompt
engineering — and about prompt injection — than a slide on either.

Common stumbles: forgetting `type="messages"` (Gradio's older tuple format has
a different shape), and yielding the delta instead of the accumulated string
(you get one character at a time in the UI).
-->

---

# 🧪 Lab: Pull the network cable (15 min)

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

**What to notice**

- `HF_HUB_OFFLINE=1` — this is a proof, not a config
- Weights come from a folder in the repo
- No key, no network, no bill, no data leaving the box
- Same Gradio wrapper as Lab A

1. Run it, then **turn off your wifi and run it again.** Note where quality drops off vs Lab A — that gap is what the rest of the week is about closing.

Done when: A chatbot answering with the network disabled.

<!--
The wifi-off step is the entire point. Do it at the front of the room too.

PREP REQUIRED — see offline_models.md for the vetted models and the sharding
recipe. Weights ship in the workshop repo, under GitHub's 100 MB per-file
limit, so participants clone rather than download on venue wifi. Pre-stage this;
do not have thirty people hit HuggingFace simultaneously.

One honest discrepancy to resolve before delivery: the outline budgets ~500 MB
for the generative model, but the smallest decent instruct model
(Qwen2.5-0.5B-Instruct) is ~1 GB in fp16. Either accept ~1 GB, or ship a
quantised build to hit 500 MB. The 85 MB arctic-embed-xs embedding model is
comfortably within budget either way and is what M4's offline RAG uses.

Expect the quality gap to be stark and USE IT. Do not apologise for it — ask
the room what would have to be true for the small model to be good enough for
one specific job. Answers: a narrower task, a better prompt, retrieved context,
fine-tuning. Those are M2, M3, M4, and M6. This lab is the setup for the week.

Alternative labs if a group finishes early or wants something else: Gradio live
transcriber, text-to-image, or trend summaries over the Chronos prices CSV
from M0.
-->

---

<!-- _class: lead -->

# Where That Leaves Us

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
