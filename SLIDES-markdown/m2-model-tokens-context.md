---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M2.0.1 · Model, Tokens & Context

What you're actually buying

By the end of this module you can:

- Explain what a token is, and count them before you send
- Say what the context window holds, and what falls out when it's full
- Predict and measure what a feature costs
- Choose a model size deliberately — and route between sizes
- Explain what an embedding is, and why tomorrow depends on it

<!--
~75 minutes, last 25 hands-on.

Frame this as an engineering inspection of the call they already wrote in M1.
Open the black box only far enough to explain cost, latency, context failures,
and hallucination. This is not a machine-learning theory module.

No new ways to call a model in this module. Everything here dissects the call
they already wrote in M1.
-->

---

**Anatomy · 1/2**

# M2.1.1 · One Call, Labelled

```python
"""Way 1: closed model, straight from the vendor."""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)
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

Callback file: `SLIDES-markdown/m1/first_call.py`

**You wrote this yesterday**

| Part | What it is |
|---|---|
| `model` | Which brain. Size, speed, price. |
| `system` | Standing instructions *(not shown)* |
| `messages` | The conversation so far |
| `max_tokens` | A cap on the **reply** |

Three inputs — **model**, **prompt**, **context** — and one output.

Everything in this module is one of those three.

<!--
Use the same call shape from M1. The point is continuity: they already know how
to call a model; now they inspect what each line controls and what it costs.

The one correction people need here: max_tokens caps the RESPONSE, not the
request. It is not a budget for the whole call and it is not visible to the
model. Sizing it too small is the most common first bug — you get a reply that
stops mid-sentence and stop_reason "max_tokens".

Nothing on this slide is a new API. It is a re-orientation before the mechanics.
-->

---

**Anatomy · 2/2**

# M2.1.2 · There Is No Conversation

```python
"""There is no conversation on the server."""

messages = []


def turn(question: str, answer: str) -> None:
    messages.append({"role": "user", "content": question})
    # ... the API call goes here ...
    messages.append({"role": "assistant", "content": answer})
    print(f"sent {len(messages)} messages this turn")


turn("What do I hold?", "SPY, QQQ and GLD.")        # sent 2
turn("Which is largest?", "SPY, at 52%.")           # sent 4
turn("Is that risky?", "Yes. Concentrated.")        # sent 6

# Turn 3 resent turns 1 and 2. You paid for them again.
# "Memory" is just you resending the whole transcript.
```

Full running version: `SLIDES-markdown/m2/growing_messages.py`

**What to notice**

- Nothing is stored on the server between calls
- Turn 3 resends turns 1 and 2 — in full
- The transcript is the only memory that exists
- You pay for the whole thing, **every turn**

M1 said the API is stateless. This is what stateless costs: a 40-turn chat sends turn 1 forty times.

<!--
M1 asserted statelessness. This slide shows the cost. Three later topics depend
on it: long chats get expensive, the context window fills, and caching exists
because stable prefixes are resent.

Draw the growth on the board if it helps — turn 1 sends 2 messages, turn 10
sends 20, turn 40 sends 80. Cost per turn rises linearly through a conversation
even though the user's question stays the same size.

If students ask how chat products remember, answer precisely: the application
rebuilds a transcript on every request, often with retrieved user/profile/task
data added. That is application memory, not model memory.
-->

---

**The Mechanism · 1/3**

# M2.2.1 · Prompt → Tokens → Token IDs

```python
"""Prompt -> Tokens -> Token IDs. Look inside."""

from transformers import AutoTokenizer

PATH = "../OFFLINE-AI-Models/smollm2-135m-instruct"
tok = AutoTokenizer.from_pretrained(
    PATH, local_files_only=True
)

text = "Chronos rebalances portfolios internationally."

ids = tok.encode(text)

print(len(ids), "tokens for", len(text), "characters")
for i in ids:
    print(f"{i:>7}  {tok.decode([i])!r}")

# 'Ch' 'ron' 'os' ' reb' 'al' 'ances' ' portfolios'
# ' international' 'ly' '.'
#
# The IDs are this model's; run it and read your own.
# A token is a frequent chunk of text.
# Not a word. Not a letter. Something in between.
```

Full running version: `SLIDES-markdown/m2/token_ids.py`

**What to notice**

- Text is split into **frequent chunks**, not words
- Common words are one token; rare ones split
- The leading space is part of the token
- Each chunk maps to an integer — that's all the model sees

The model never sees your text. It sees a list of numbers.

<!--
Run this live if possible. Many students assume tokens are words until they see
a word split into chunks.

This uses an open model tokenizer because vendor tokenizers may not be public.
The behavior is similar across modern models — frequent chunks, leading spaces
attached — but exact counts differ by model. Use `count_tokens` on the next
slide for a local estimate before you spend cloud tokens.

Things worth pointing at in the output: " portfolios" with the leading space is
one token; a rare product name will shatter into 4-5 tokens; whitespace and
punctuation cost real money.
-->

---

<!-- _class: lead -->

**The Mechanism · 2 of 3**

# M2.2.2 · It Predicts The Next Token

That is the entire mechanism.

Given everything so far → what token comes next?
Append it. Repeat.

<!--
This is the central mechanism slide. Everything before it sets up the
mechanism; everything after it is a consequence.

Say it plainly: there is no lookup, no database, no fact-checking step. The
model computes a probability over the next token given all preceding tokens,
picks one, appends it, and does it again. That is the loop, all the way to the
end of the answer.

Pause after stating the mechanism. The key implication is that truth is not a
separate runtime check. The model is optimizing the next token, not verifying a
fact against a database.

Do not go further into architecture. No attention diagrams, no transformer
blocks, no training discussion. It is not needed to build anything, and it is the single
easiest place in this workshop to lose ninety minutes.
-->

---

**The Mechanism · 3/3**

# M2.2.3 · What That One Fact Explains

| Behaviour | Because |
|---|---|
| Fluent, confident, and **wrong** | Plausible-next-token ≠ true. Nothing checks. |
| Can't count the r's in "strawberry" | It never saw letters. It saw 2–3 chunks. |
| Hindi or Marathi costs more per sentence | Fewer common chunks → more tokens per word |
| Rarely says "I don't know" | "I don't know" is rarely the likely next token |
| Better with context than without | More preceding tokens → better-conditioned guess |

If output is predicted from context, then controlling context is the job.

<!--
This slide explains M1's "wrong, slow, forgetful" observations. The failures
stop being mysterious when tied to a mechanism.

The hallucination framing should be technical: the model is not running a truth
checker. It is producing likely text. To improve correctness, change what it is
conditioned on, validate the output, retrieve facts, or narrow the task.

The strawberry example is worth demoing live if you have a small model handy.

Prompt engineering, RAG, and fine-tuning are different ways to control behavior
and context. This connects directly to M3, M4, and M6.
-->

---

**The Context Window · 1/4**

# M2.3.1 · Count Before You Send

```python
"""Count before you send. The only honest estimate."""

from chronos_offline import count_tokens

POLICY = open("data/investment_policy.md").read()

print(len(POLICY.split()), "words")
print(count_tokens(POLICY), "tokens")

JSON = '{"symbol":"AAPL"}'
for text in ["portfolio", "Rebalancing", "AAPL", JSON,
             "पोर्टफोलियो"]:
    print(f"{count_tokens(text):>3}  {text}")
```

Full running version: `SLIDES-markdown/m2/count_tokens.py`

**Why bother**

- Local and exact for the model you actually call
- Word counts are wrong by 30%+ on code
- Lets you price a feature *before* you build it
- Lets you check something fits before sending it

**Never use the wrong tokenizer.** Token counts are model-specific.

<!--
Practical habit: before shipping a feature, run one representative request
through `count_tokens`, multiply by expected volume, and multiply by the price.
That turns cost into an engineering decision before implementation.

Worked example on the board, using their Chronos portfolio explanations:
  2,000 tokens/call x 50,000 calls/day = 100M tokens/day
  At $5/1M input, that is $500/day on input alone. Is the feature worth $15k a
  month? Sometimes yes. But now it's a decision instead of a surprise.

The `tiktoken` warning is not pedantry. It returns plausible numbers for the
wrong tokenizer. Plausible undercounts are worse than obvious errors.
-->

---

**The Context Window · 2/4**

# M2.3.2 · The Window Holds Everything

**What's in there**

- The system prompt
- Every previous turn, in full
- Tool definitions and tool results
- Files, images, retrieved documents
- The reply being generated

**Rough sizes**

| Model | Window |
|---|---|
| Gemini 2.5 Flash-Lite | 1M tokens |
| Gemini 2.5 Flash | 1M tokens |
| Small open models | 8K–128K |

A big window is a ceiling, not an allowance.

You pay for every token you actually put in it, on every turn.

<!--
The mental model correction: a context window is a limit, not free storage.
Filling a large window is expensive before the model generates a single output
token.

The other half people miss: it's not just chat history. Tool definitions sit in
there on every call. A big system prompt sits in there on every call. In an
agentic app (M7) the tool schemas alone can dominate.

Numbers date — re-check the window column before delivery.
-->

---

**The Context Window · 3/4**

# M2.3.3 · When It Fills Up

```python
"""The window is finite. Decide what falls out."""

KEEP_TURNS = 20


def trim(messages: list[dict]) -> list[dict]:
    """Drop the oldest turns, keep the conversation valid."""
    keep = messages[-KEEP_TURNS:]

    # A transcript must start on a user turn, and a tool
    # result must never be orphaned from its tool call.
    while keep and keep[0]["role"] != "user":
        keep.pop(0)
    return keep


# How you find out you overflowed -- check stop_reason:
#
#   "max_tokens"
#       The REPLY was cut off mid-sentence.
#       Fix: raise max_tokens, or stream.
#
#   "model_context_window_exceeded"
#       The INPUT no longer fits.
#       Fix: trim old turns, or summarise them.
#
# Trimming forgets. Summarising remembers, but costs a call.
```

Full running version: `SLIDES-markdown/m2/window_full.py`

**Two different failures**

- `max_tokens` — the **reply** got cut off. Raise the cap, or stream.
- `model_context_window_exceeded` — the **input** no longer fits. Trim or summarise.

Trimming forgets.

Summarising remembers, but costs a call.

Pick deliberately.

<!--
Both failures show up as a stop_reason, which is why M1's production slide made
checking it a habit. Callback to that explicitly.

The trimming pitfalls are practical: a transcript must start on a user turn,
and a tool result must not be separated from the tool call that produced it.
Both mistakes can produce API errors that look unrelated to trimming.

Summarising or compaction replaces old turns with a shorter representation.
That can preserve intent, but it is lossy and costs another model call. M9
returns to this trade-off when implementing conversation memory.

Worth naming: "how much should the bot remember?" is a product question, not an
infrastructure one. A support bot needs the whole ticket. A search box needs
nothing. Decide it, don't inherit it from a default.
-->

---

**The Context Window · 4/4**

# M2.3.4 · Caching: Stop Paying Twice

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=f"Policy:\n{POLICY}\n\nQuestion: {question}",
)

u = response.usage_metadata
print(u.prompt_token_count)
print(u.candidates_token_count)
```

Full running version: `SLIDES-markdown/m2/caching.py`

**What to notice**

- Keep the **stable** policy prefix separate in your code
- Only the user question should change turn to turn
- Usage metadata tells you what the call consumed
- The full running file uses Gemini Flash Lite from `.env`

Provider caching works best when stable content is a **prefix**.

One changed byte and everything after it misses.

<!--
This follows directly from statelessness. The app resends stable content, but
the provider can discount a stable cached prefix.

Order matters and it follows from the prefix rule: stable content first,
volatile content last. A long policy or instruction set goes before the user's
question. The question changes; the policy should not.

Debugging habit: if a provider-side cache never hits across repeated calls,
something in the prefix is changing. Usual suspects — a datetime, a UUID, a
per-user ID interpolated into the system prompt, or a tool list built in
non-deterministic order.

One caveat: prompts below the minimum cacheable size silently don't cache. No
error, just zeros. If it "isn't working", check the prefix is long enough.
-->

---

<!-- _class: lead -->

**Size & Cost · 1/4**

# M2.4.1 · Quality Depends On Something Inside The Model

What do you think it is?

<!--
Pause here and ask for guesses.

Expected answers include training data, training time, architecture, and money
spent. They are partly true, but the engineering proxy to introduce is
parameters: learned weights.

The answer you're steering to: PARAMETERS. The number of learned weights. It
sets both how much the model absorbed during training and how much reasoning it
can do per token generated.

Connect this to M1's offline model. A small local model is weaker because it has
far fewer learned weights and less capacity. That is not a broken install; it
is the trade made to run locally.
-->

---

**Size & Cost · 2/4**

# M2.4.2 · IQ vs Size vs Cost

| Class | Parameters | Runs on | Cost / 1M | Good for |
|---|---|---|---|---|
| **Edge** | <1B | Phone, browser | ~free | Classification, autocomplete |
| **Small** | 1–10B | One laptop / CPU | cents | Extraction, routing, narrow tasks |
| **Medium** | 10–100B | One or two GPUs | $ | Most production features |
| **Large** | 100B+ | A GPU cluster | $$–$$$ | Hard reasoning, long agentic work |

Three things move together:

```text
more parameters -> more capability -> more cost and latency
```

<!--
The table is a shape, not a spec sheet — parameter boundaries are fuzzy and
mixture-of-experts models muddy "parameters" considerably (a 400B MoE model may
only activate 30B per token). Don't over-defend the numbers.

The engineering point: start with the smallest class that could plausibly work
and move up when evals show it is necessary. That requires evaluation, which is
M3.

Second point worth making: capability is not one axis. A small model fine-tuned
on your task can beat a frontier model at that one task — which is the entire
argument for M6, and it's why "just use the biggest model" is not a strategy.
-->

---

**Size & Cost · 3/4**

# M2.4.3 · Model Routing

```python
def is_simple(question: str) -> bool:
    """Classify by meaning. Local, fast, no tokens billed."""
    q = embed([question])[0]
    return similarity(q, simple_v) > similarity(q, hard_v)


def answer(question: str) -> str:
    if is_simple(question):
        return cheap_model(question)
    return frontier_model(question)
```

Full running version: `SLIDES-markdown/m2/routing.py`

**The trade**

- A local embedding comparison decides the model
- Easy questions never touch the expensive model
- Costs one extra round trip
- Pays for itself when the split is real

Model tiers can differ by orders of magnitude in cost.

Routing is how a product captures that spread.

<!--
Direct callback to M1's model-access decision. Different model tiers have
different cost and latency. Routing makes that difference operational.

Be honest about when routing does NOT pay: if 90% of your traffic is genuinely
hard, you have added latency and a classifier to save nothing. Measure the split
before building the router.

Cheaper variants worth mentioning: route on a keyword or a regex rather than a
model call; route on which UI surface the request came from; let the cheap model
answer and escalate only when it signals low confidence. The router does not
have to be an LLM.

Failure mode: a hard question misrouted to a weak model gets a bad answer
silently. Log the chosen route and model for every request.
-->

---

**Size & Cost · 4/4**

# M2.4.4 · Bigger Is Also Slower

**Where the time goes**

- **Time to first token** — the model reads your whole context
- **Then ~n tokens/second** — bigger model, fewer per second
- Long context makes the first part worse
- Thinking/reasoning modes generate *more* tokens

**What you can do**

- Stream — you saw this in M1
- Route small where you can
- Send less context
- Cache the prefix so the read is cheap

Streaming does not reduce total generation time.

It reduces perceived wait by showing tokens as they arrive.

<!--
"Slow" was one of M1's three observed complaints. This slide gives the latency
mechanism.

The distinction that helps engineers reason about latency: time-to-first-token
scales with how much you sent; tokens-per-second is a property of the model.
Those are two different problems with two different fixes. Sending less context
helps the first. A smaller model helps the second.

Streaming is a UX intervention, not a throughput improvement. Both kinds of
improvement matter, but they solve different problems.
-->

---

**Meaning · 1 of 1**

# M2.5.1 · Token IDs → Meaning

```python
"""A token becomes numbers that mean something."""

from chronos_offline import embed, similarity

vectors = embed([
    "broad market index fund",       # 0
    "S&P 500 tracker",               # 1
    "leather office chair",          # 2
])

print(vectors.shape)        # (3, 384)
print(round(similarity(vectors[0], vectors[1]), 3))
print(round(similarity(vectors[0], vectors[2]), 3))

# "index fund" and "S&P 500 tracker" share one character.
# Nothing here matched a word. It matched MEANING.
#
# Tomorrow you will search over these numbers instead of
# searching over words. That is the whole idea of RAG.
```

Full running version: `SLIDES-markdown/m2/embeddings.py`

**What to notice**

- Every piece of text becomes a fixed-length list of numbers
- Similar meanings land **close together**
- "index fund" and "S&P 500 tracker" share one character — and still match
- Comparing two vectors is arithmetic, and it's fast

This is the same 85 MB model from M0.

It does one job: turn meaning into numbers.

<!--
This is the bridge into RAG. If students understand text as vectors, M4 becomes
a retrieval system rather than a magic search box.

The intuition that works: a vector is a location. Meaning becomes a position in
space, and things that mean similar things end up near each other. You are not
comparing letters, you are measuring distance.

Keep it concrete and avoid unnecessary math. Nobody needs cosine similarity derived;
they need to see that "index fund" and "S&P 500 tracker" score high while it
and "office chair" score low, with zero overlapping characters. That single
demo does all the work.

Callback: this is the arctic-embed-xs model from M0's HuggingFace slide. Two
modules later, the thing that looked like a toy download is doing real work.
-->

---

# M2.L1 · Lab: Instrument The Chatbot You Already Built

Open your M1 Gradio app. Don't start a new file.

1. Print `usage.input_tokens` and `usage.output_tokens` after each reply
2. Add a **running dollar cost** to the UI — watch it climb as you chat
3. Trim history to the last N turns; keep chatting until it **forgets** something
4. Add a model dropdown (Haiku / Opus) and ask both the same hard question
5. Cache the system prompt; check `cache_read_input_tokens` is non-zero

Done when: the chatbot shows what each turn cost, and you can estimate one day
of traffic.

<!--
The point of building on yesterday's file is compounding. Students should leave
with one app that keeps growing, not a new throwaway script for every concept.

Step 3 is the important memory experiment. Trim aggressively (5 turns), then reference
something from turn 1 and watch it fail. Seeing "forgetful" happen on purpose,
under their own control, is what turns it from a mystery into a parameter.

Step 4 usually surprises people twice: Haiku is much better than expected on
easy questions, and much worse on the hard one. Both halves matter — that gap is
exactly what makes routing worth building.

Step 5 is the fiddly one. If cache_read_input_tokens stays zero, the usual cause
is a system prompt shorter than the minimum cacheable length. Have a long
policy document ready to paste.

If a group finishes early: have them build the router from the routing slide and
measure what it saves across 20 mixed questions.
-->

---

<!-- _class: lead -->

# M2.6.1 · You Can Now Read The Bill

You know what a token is, what the window holds, and what it costs.

You know the model predicts the next token — and why that makes it fluent and confidently wrong.

Next: **five ways to build with it.**

<!--
Close the loop on M1's three complaints — all three now have mechanisms:
  wrong      -> next-token prediction, and model size
  slow       -> parameters and context length
  forgetful  -> the context window and what you trim

Then set up M3 with the line from the "what that one fact explains" slide: if
output is predicted from context, controlling context is the job. The five
patterns in M3 are five different levels of control over what goes into that
window — from just asking nicely, up to an agent that fetches its own context.

Bridge sentence: "you now understand one call. Tomorrow is about what you build
out of many of them."
-->
