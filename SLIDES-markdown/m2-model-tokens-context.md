---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M2 · Model, Tokens & Context

What you're actually buying

By the end of this module you can:

- Explain what a token is, and count them before you send
- Say what the context window holds, and what falls out when it's full
- Predict and measure what a feature costs
- Choose a model size deliberately — and route between sizes
- Explain what an embedding is, and why tomorrow depends on it

<!--
~75 minutes, last 25 hands-on.

The framing to open with: yesterday the model was a black box that worked. Today
we open it — but only far enough to explain the bill and the failure modes. We
are not doing machine learning. We are doing "what am I paying for, and why did
it do that".

No new ways to call a model in this module. Everything here dissects the call
they already wrote in M1.
-->

---

**Anatomy · 1/2**

# One Call, Labelled

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

**You wrote this yesterday**

| Part | What it is |
|---|---|
| `model` | Which brain. Size, speed, price. |
| `system` | Standing instructions *(not shown)* |
| `messages` | The conversation so far |
| `max_tokens` | A cap on the **reply** |

Three inputs — **model**, **prompt**, **context** — and one output. Everything in this module is one of those three.

<!--
Deliberately the same file from M1, not a new one. Say that out loud: "you have
already written this; today we find out what each line costs you."

The one correction people need here: max_tokens caps the RESPONSE, not the
request. It is not a budget for the whole call and it is not visible to the
model. Sizing it too small is the most common first bug — you get a reply that
stops mid-sentence and stop_reason "max_tokens".

Nothing on this slide is new information. It's a re-orientation, and it should
take four minutes.
-->

---

**Anatomy · 2/2**

# There Is No Conversation

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

**What to notice**

- Nothing is stored on the server between calls
- Turn 3 resends turns 1 and 2 — in full
- The transcript is the only memory that exists
- You pay for the whole thing, **every turn**

M1 said the API is stateless. This is what stateless costs: a 40-turn chat sends turn 1 forty times.

<!--
M1 asserted statelessness on a bullet. This slide is the proof, and it is worth
the time because three later things depend on it: why long chats get expensive,
why the context window fills up, and why caching exists at all.

Draw the growth on the board if it helps — turn 1 sends 2 messages, turn 10
sends 20, turn 40 sends 80. Cost per turn rises linearly through a conversation
even though the user's question stays the same size.

Someone always asks "so how do chat products remember me?" Good question, and
the answer is: they don't, the server-side app re-assembles a transcript (plus
retrieved notes) on every request. That's M4 and it's worth naming here.
-->

---

**The Mechanism · 1/3**

# Prompt → Tokens → Token IDs

```python
"""Prompt -> Tokens -> Token IDs. Look inside."""

from transformers import AutoTokenizer

MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
tok = AutoTokenizer.from_pretrained(MODEL)

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

**What to notice**

- Text is split into **frequent chunks**, not words
- Common words are one token; rare ones split
- The leading space is part of the token
- Each chunk maps to an integer — that's all the model sees

The model never sees your text. It sees a list of numbers.

<!--
Run this live. It gets a genuine reaction, because everyone assumes tokens are
words until they watch "internationally" break into two pieces.

HONESTY POINT, say it: this uses an open model's tokeniser because Claude's is
not public. The *behaviour* is the same across modern models — frequent chunks,
leading spaces attached — but the exact splits and counts differ. For real
Claude numbers, use count_tokens (next slide).

Things worth pointing at in the output: " portfolios" with the leading space is
one token; a rare product name will shatter into 4-5 tokens; whitespace and
punctuation cost real money.
-->

---

<!-- _class: lead -->

**The Mechanism · 2/3**

# It predicts the next token.

That is the entire mechanism.

Given everything so far → what token comes next?
Append it. Repeat.

<!--
THE slide of the module. Slow down. Everything before it was setup and
everything after it is a consequence.

Say it plainly: there is no lookup, no database, no fact-checking step. The
model computes a probability over the next token given all preceding tokens,
picks one, appends it, and does it again. That is the loop, all the way to the
end of the answer.

Then let it sit for a second before the next slide, because the room needs a
beat to realise what that implies. Someone usually gets there on their own:
"...so it has no idea whether what it's saying is true?" Correct.

Do NOT go further into architecture. No attention, no transformers diagram, no
training discussion. It is not needed to build anything, and it is the single
easiest place in this workshop to lose ninety minutes.
-->

---

**The Mechanism · 3/3**

# What That One Fact Explains

| Behaviour | Because |
|---|---|
| Fluent, confident, and **wrong** | Plausible-next-token ≠ true. Nothing checks. |
| Can't count the r's in "strawberry" | It never saw letters. It saw 2–3 chunks. |
| Hindi or Marathi costs more per sentence | Fewer common chunks → more tokens per word |
| Rarely says "I don't know" | "I don't know" is rarely the likely next token |
| Better with context than without | More preceding tokens → better-conditioned guess |

> The last row is the entire rest of this workshop. **If output is predicted from context, then controlling context is the job.**

<!--
This is where "wrong, slow and forgetful" from M1's close gets its answer, and
the room usually relaxes visibly — the failures stop feeling like the model
being broken and start feeling like a mechanism they understand.

The hallucination framing that lands best: it is not lying and it is not
malfunctioning. It is doing exactly what it does — producing likely text. Truth
is not part of the objective. That reframe matters because it tells you where to
intervene: you cannot ask it to try harder to be right; you have to change what
it is conditioning on.

The strawberry example is worth demoing live if you have a small model handy.

Land the final line hard. Prompt engineering, RAG, and fine-tuning are three
different answers to the same question: how do we control what it conditions on?
That's M3, M4, and M6.
-->

---

**The Context Window · 1/4**

# Count Before You Send

```python
"""Count before you send. The only honest estimate."""

from anthropic import Anthropic

client = Anthropic()

POLICY = open("data/mini_policy.md").read()

n = client.messages.count_tokens(
    model="claude-opus-5",        # counts are model-specific
    system="You are Chronos's portfolio assistant.",
    messages=[{"role": "user", "content": POLICY}],
)

print(n.input_tokens)

# Costs nothing, takes one round trip, and is exact.
#
# Do NOT estimate with a word count -- you will be out by
# 30%+ on code and on non-English text.
# Do NOT use tiktoken. That is OpenAI's tokeniser.
```

**Why bother**

- One round trip, costs nothing, exact
- Word counts are wrong by 30%+ on code
- Lets you price a feature *before* you build it
- Lets you check something fits before sending it

**Never use `tiktoken` for Claude.** It's OpenAI's tokeniser — it undercounts by 15–20%, worse on code.

<!--
The practical habit: before shipping a feature, run one representative request
through count_tokens, multiply by expected volume, multiply by the price. That
number has killed more bad AI feature ideas than any architecture review, and it
takes two minutes.

Worked example on the board, using their Chronos portfolio explanations:
  2,000 tokens/call x 50,000 calls/day = 100M tokens/day
  At $5/1M input, that is $500/day on input alone. Is the feature worth $15k a
  month? Sometimes yes. But now it's a decision instead of a surprise.

The tiktoken warning is not pedantry. It is the single most common token-math
mistake, because tiktoken is easy to pip install and returns a plausible number.
-->

---

**The Context Window · 2/4**

# The Window Holds Everything

**What's in there**

- The system prompt
- Every previous turn, in full
- Tool definitions and tool results
- Files, images, retrieved documents
- The reply being generated

**Rough sizes**

| Model | Window |
|---|---|
| Claude Opus 5 | 1M tokens |
| Claude Haiku 4.5 | 200K |
| Small open models | 8K–128K |

> A big window is not free. **It's a ceiling, not an allowance** — you pay for every token you actually put in it, on every single turn.

<!--
The mental model correction that matters: people hear "1M token context" and
think of it as storage they've been given. It is a limit, not a quota — filling
it costs real money every turn, and a 500K-token conversation is expensive
before the model has said anything.

The other half people miss: it's not just chat history. Tool definitions sit in
there on every call. A big system prompt sits in there on every call. In an
agentic app (M7) the tool schemas alone can dominate.

Numbers date — re-check the window column before delivery.
-->

---

**The Context Window · 3/4**

# When It Fills Up

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

**Two different failures**

- `max_tokens` — the **reply** got cut off. Raise the cap, or stream.
- `model_context_window_exceeded` — the **input** no longer fits. Trim or summarise.

**Trimming forgets. Summarising remembers, but costs a call.** Pick deliberately — this is the "forgetful" from yesterday, and it's a design decision, not a bug.

<!--
Both failures show up as a stop_reason, which is why M1's production slide made
checking it a habit. Callback to that explicitly.

The trimming pitfalls are real and they bite in week one: a transcript must
start on a user turn, and you must never orphan a tool_result from the tool_use
that produced it. Both throw a 400 that reads like nonsense if you don't know.

Summarising (compaction) is the grown-up version — you replace old turns with a
model-written summary. The API has server-side compaction as a beta feature, or
you roll your own. Mention it exists; don't teach it here.

Worth naming: "how much should the bot remember?" is a product question, not an
infrastructure one. A support bot needs the whole ticket. A search box needs
nothing. Decide it, don't inherit it from a default.
-->

---

**The Context Window · 4/4**

# Caching: Stop Paying Twice

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=4096,
    system=[
        {
            "type": "text",
            "text": POLICY,         # long, and never changes
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=messages,              # short, changes each turn
)

u = response.usage
print(u.cache_creation_input_tokens)   # written: 1.25x cost
print(u.cache_read_input_tokens)       # reused:  0.10x cost
print(u.input_tokens)                  # fresh:   full price
```

**What to notice**

- Mark the **stable** part; leave the volatile part unmarked
- Cache reads cost ~**0.1×**; writes cost ~1.25×
- Breaks even on the second request
- `usage` tells you whether it actually worked

It's a **prefix** match. One changed byte and everything after it misses — which is why a timestamp in the system prompt is the classic silent bug.

<!--
This pays off the promise M1 made when it taught statelessness: yes you resend
everything every turn, and no, you don't have to pay full price for it.

Order matters and it follows from the prefix rule: stable content first,
volatile content last. A long policy or instruction set goes in system with
the marker. The user's question goes after and stays unmarked.

The debugging habit worth teaching: if cache_read_input_tokens is zero across
repeated calls, something in the prefix is changing. Usual suspects — a
datetime, a UUID, a per-user ID interpolated into the system prompt, or a tool
list built in non-deterministic order.

One caveat: prompts below the minimum cacheable size silently don't cache. No
error, just zeros. If it "isn't working", check the prefix is long enough.
-->

---

<!-- _class: lead -->

**Size & Cost · 1/4**

# Quality depends on something inside the model.

What do you think it is?

<!--
STOP HERE. Ask it, then wait. Count to ten in your head if you have to.

This is deliberately a pause, not a rhetorical flourish. Let the room guess —
you will get "training data", "how long it was trained", "the algorithm", "how
much money they spent". All reasonable, all partly true.

The answer you're steering to: PARAMETERS. The number of learned weights. It
sets both how much the model absorbed during training and how much reasoning it
can do per token generated.

Then connect it straight back to something they physically experienced
yesterday: the offline model in M1's lab was worse, and now they know why —
0.5 billion parameters against several hundred billion. That is not a bug or a
bad download. That is the trade they made when they chose a model that fits on
a laptop.
-->

---

**Size & Cost · 2/4**

# IQ vs Size vs Cost

| Class | Parameters | Runs on | Cost / 1M | Good for |
|---|---|---|---|---|
| **Edge** | <1B | Phone, browser | ~free | Classification, autocomplete |
| **Small** | 1–10B | One laptop / CPU | cents | Extraction, routing, narrow tasks |
| **Medium** | 10–100B | One or two GPUs | $ | Most production features |
| **Large** | 100B+ | A GPU cluster | $$–$$$ | Hard reasoning, long agentic work |

Three things move together: **more parameters → more capability → more cost and more latency.** There is no setting where you get one without the others.

<!--
The table is a shape, not a spec sheet — parameter boundaries are fuzzy and
mixture-of-experts models muddy "parameters" considerably (a 400B MoE model may
only activate 30B per token). Don't over-defend the numbers.

The engineering point: most teams reach for the biggest model by default and
then complain about the bill. The discipline is to start at the smallest class
that could plausibly work and move up only when your evals say you must. That
requires evals, which is M3.

Second point worth making: capability is not one axis. A small model fine-tuned
on your task can beat a frontier model at that one task — which is the entire
argument for M6, and it's why "just use the biggest model" is not a strategy.
-->

---

**Size & Cost · 3/4**

# Model Routing

```python
def is_simple(question: str) -> bool:
    """One tiny Haiku call. Costs ~5 output tokens."""
    out = client.messages.create(
        model=CHEAP,
        max_tokens=5,
        system="Reply with one word: SIMPLE or HARD.",
        messages=[{"role": "user", "content": question}],
    )
    return out.content[0].text.strip() == "SIMPLE"


def answer(question: str) -> str:
    model = CHEAP if is_simple(question) else SMART
    out = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": question}],
    )
    return out.content[0].text
```

**The trade**

- A ~5-token Haiku call decides the model
- Easy questions never touch the expensive model
- Costs one extra round trip
- Pays for itself when the split is real

M1 showed a **~100× price spread** between model tiers. Routing is how you actually collect it.

<!--
Direct callback to M1's price-spread note — that slide set this one up.

Be honest about when routing does NOT pay: if 90% of your traffic is genuinely
hard, you have added latency and a classifier to save nothing. Measure the split
before building the router.

Cheaper variants worth mentioning: route on a keyword or a regex rather than a
model call; route on which UI surface the request came from; let the cheap model
answer and escalate only when it signals low confidence. The router does not
have to be an LLM.

The failure mode to warn about: a misrouted hard question gets a bad answer
silently. Log which model served each request, or you cannot debug quality
complaints at all.
-->

---

**Size & Cost · 4/4**

# Bigger Is Also Slower

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

> Streaming doesn't make it faster. It makes the wait **visible**, which users forgive.

<!--
"Slow" was the second of M1's three complaints. This closes it.

The distinction that helps engineers reason about latency: time-to-first-token
scales with how much you sent; tokens-per-second is a property of the model.
Those are two different problems with two different fixes. Sending less context
helps the first. A smaller model helps the second.

The streaming line is the honest one and it's worth saying plainly — total time
is unchanged, perceived time collapses. That's a UX intervention, not a
performance one, and both are legitimate.
-->

---

**Meaning**

# Token IDs → Meaning

```python
"""A token becomes numbers that mean something."""

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("./models/arctic-embed-xs")

vectors = model.encode([
    "broad market index fund",       # 0
    "S&P 500 tracker",               # 1
    "leather office chair",          # 2
])

print(vectors.shape)        # (3, 384)

sim = model.similarity(vectors, vectors)
print(round(float(sim[0][1]), 2))   # 0 vs 1 -> high
print(round(float(sim[0][2]), 2))   # 0 vs 2 -> low

# "index fund" and "S&P 500 tracker" share one character.
# Nothing here matched a word. It matched MEANING.
#
# Tomorrow you will search over these numbers instead of
# searching over words. That is the whole idea of RAG.
```

**What to notice**

- Every piece of text becomes a fixed-length list of numbers
- Similar meanings land **close together**
- "index fund" and "S&P 500 tracker" share one character — and still match
- Comparing two vectors is arithmetic, and it's fast

This is the same 85 MB model you downloaded in M0. It does one job: turn meaning into numbers.

<!--
This is the hinge of the whole week — land it and RAG feels inevitable
tomorrow; skip it and M4 becomes a magic trick.

The intuition that works: a vector is a location. Meaning becomes a position in
space, and things that mean similar things end up near each other. You are not
comparing letters, you are measuring distance.

Keep it concrete and resist the maths. Nobody needs cosine similarity derived;
they need to see that "index fund" and "S&P 500 tracker" score high while it
and "office chair" score low, with zero overlapping characters. That single
demo does all the work.

Callback: this is the arctic-embed-xs model from M0's HuggingFace slide. Two
modules later, the thing that looked like a toy download is doing real work.
-->

---

# 🧪 Lab: Instrument the chatbot you already built (25 min)

Open your M1 Gradio app. Don't start a new file.

1. Print `usage.input_tokens` and `usage.output_tokens` after each reply
2. Add a **running dollar cost** to the UI — watch it climb as you chat
3. Trim history to the last N turns; keep chatting until it **forgets** something
4. Add a model dropdown (Haiku / Opus) and ask both the same hard question
5. Cache the system prompt; check `cache_read_input_tokens` is non-zero

Done when: A chatbot that shows you what each turn cost, and a number you can quote for what a day of this would cost.

<!--
The point of building on yesterday's file is compounding — they should leave
with one app that keeps growing, not five throwaway scripts.

Step 3 is the one to insist on. Trim aggressively (5 turns), then reference
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

# You Can Now Read the Bill

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
