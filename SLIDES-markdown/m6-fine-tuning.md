---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M6 · LLM Fine-Tuning

Changing the model itself

By the end of this module you can:

- Decide between RAG, a prompt, and a fine-tune — and defend it
- Explain what a model *is*, in PyTorch terms, without hand-waving
- Say why LoRA/QLoRA make this affordable, and set `r` and `alpha`
- Build a training set from ~300 seeds and know what to throw away
- Measure a fine-tune with numbers a compliance officer would accept

<!--
~60 minutes of lecture, then a 60-minute lab.

The framing to open with, and to keep returning to: RAG changes what the model
KNOWS. Fine-tuning changes how it BEHAVES. Most teams reach for fine-tuning
when they needed RAG, burn six weeks and a GPU budget, and end up with a model
that is confidently wrong in a nicer voice.

This is also the module where M0's "customisable IP" promise gets cashed in.
Fine-tuning an open model on data only you have is the part of an AI stack a
competitor cannot copy by switching API keys. Say that out loud.

Half the module is deliberately not about training. Module 2 (internals) exists
so the room stops treating the model as a magic box, and Module 4 (data) is
where the actual work lives. The training command itself is twenty lines and
five minutes.
-->

---

<!-- _class: lead -->

**Fine-Tune or RAG · 1/5**

# Yesterday you taught it to look things up.

Today you change how it responds.

RAG changes **what it knows**.
Fine-tuning changes **how it behaves**.

<!--
The whole first section is this one distinction, and it is worth the ten
minutes because getting it wrong is expensive in a way nothing else in this
workshop is.

Ask the room for their own examples before you show the next two slides. You
will get "we want it to know our product catalogue" (that is RAG) and "we want
it to stop sounding like a chatbot" (that is fine-tuning), and having those two
sentences come from the audience makes the rest land.

The failure this prevents: a team fine-tunes on last quarter's policy documents
so the model "knows the policy", ships it, the policy changes in March, and now
the wrong answer is baked into the weights where you cannot see it or delete
it. RAG would have been a file swap.
-->

---

**Fine-Tune or RAG · 2/5**

# When Fine-Tuning Wins

**Structure** — every reply must be the same valid JSON, every time. Schema compliance, field mapping, extraction.

**Voice** — compliance-safe wording, non-promotional phrasing, the house style your reviewers already approved.

**Task shape** — a narrow job done a thousand times a day, the same way.

**Cost and latency** — a 0.5B model on your own hardware instead of a 4,000-token prompt to a frontier API on every call.

> Chronos version: *always* emit `{symbol, action, shares}` — no prose, no apology, no markdown fence.

<!--
The pattern behind all four: you are teaching a BEHAVIOUR that is stable, that
you can demonstrate hundreds of times, and that a prompt keeps failing to pin
down reliably.

The structure case is the one that actually pays in BFSI, and it is worth
dwelling on. A frontier model with a good prompt will emit valid JSON maybe
95% of the time. That sounds fine until you are parsing 50,000 advisor notes a
day, and 2,500 of them fall over. A small fine-tuned model at 99.5% is both
cheaper and better at exactly this one thing.

The cost case is the one that gets budget approved. Say the arithmetic out
loud: a 4,000-token system prompt on every call, at scale, costs more per month
than the fine-tuning run cost once. And it never stops costing it.

Do not let the room conclude fine-tuning makes a model smarter. It does not. It
makes it more RELIABLE at one narrow thing, usually at the cost of being
slightly worse at everything else.
-->

---

**Fine-Tune or RAG · 3/5**

# When RAG Wins

| You need | Why fine-tuning fails |
|---|---|
| This morning's prices, rates, holdings | Weights are frozen at training time |
| A citation back to the source document | There is no source. It's diffused into numbers. |
| To delete a client's data on request | You cannot un-train a weight. You retrain. |
| Facts that change monthly | Every change is a new training run |
| An audit trail for a regulator | "The weights decided" is not an answer |

> **Facts → RAG. Form and behaviour → fine-tune.** If you can't say which one your problem is, it's RAG.

<!--
The deletion row is the one that stops the room, and it is worth landing hard
because it is a legal exposure, not an engineering inconvenience. Under DPDP or
GDPR, "delete my data" against a fine-tuned model means retraining from the
base without that data. If a client's records were in the training set, they
are diffused across billions of weights and there is no surgical removal.

The citation row matters for the same reason. RAG can point at chunk 14 of
policy_2026.pdf. A fine-tune cannot point at anything — which is why regulated
workflows keep the FACTS in retrieval even when the FORMAT is fine-tuned.

The final rule of thumb is deliberately blunt. In a room of engineers who have
just spent a day on RAG and are excited about the new toy, defaulting to RAG is
the correct bias.
-->

---

**Fine-Tune or RAG · 4/5**

# What Production Actually Looks Like

**The fine-tuned adapter does**

- Parse the messy note
- Emit the strict schema
- Hold the compliance voice
- Run small, local, cheap

**RAG does**

- Today's prices for those symbols
- The client's current holdings
- The policy text in force *now*
- Anything with a citation

> Neither one alone. The adapter is the **shape** of the answer; retrieval fills in the **facts**. This is what BFSI systems actually ship.

<!--
This is the slide to photograph, and someone always does.

Walk one request end to end, out loud: advisor note arrives -> fine-tuned
adapter extracts {symbol, action, shares} -> that symbol is used to retrieve
today's close and the client's current position -> a frontier model (or a
template) writes the confirmation using retrieved numbers. Three components,
each doing the thing it is actually good at.

Notice the adapter never touches a number that matters. It handles language and
structure only. That is a deliberate design rule and it is worth stating: never
fine-tune a model to REMEMBER a value you could look up.

Callback to M2's routing slide — this is the same instinct one level up. Right
model, right size, right job.
-->

---

**Fine-Tune or RAG · 5/5**

# Try Them In This Order

| Approach | Time to first result | When you've earned it |
|---|---|---|
| **Prompt engineering** | Minutes | Always start here |
| **Few-shot examples** | An hour | The prompt is close but inconsistent |
| **RAG** | Days | It needs facts it doesn't have |
| **Fine-tuning** | Weeks + data + GPUs | All of the above, measured, still short |

> You need an eval before you can tell whether step 4 helped. **If you can't measure it, you can't fine-tune it** — you can only feel better about it.

<!--
This slide exists to slow people down, and it is the most useful thing in the
first section for anyone who goes back to a team next week with budget.

The honest sequencing point: almost every fine-tuning project that gets
abandoned was started at step 4. Teams skip measurement, fine-tune on a hunch,
cannot tell whether the result is better, and quietly stop talking about it.

The eval requirement is not optional gatekeeping. Fine-tuning changes the model
in ways you cannot inspect by reading the diff — there is no diff. The only
evidence you will ever have is a score on a held-out set, which means the score
has to exist BEFORE you start. That is the last slide of this module and it is
also the first thing you should build.

M3's evaluation material is the prerequisite. If they skipped it, say so.
-->

---

<!-- _class: lead -->

**Inside the Model · 1/6**

# So what is a model, actually?

Before we change one, we open one.

<!--
Transition slide. Fifteen minutes on internals, and the reason to spend them is
that everything in the second half — VRAM, ranks, learning rates, overfitting —
is unreadable if the model is still a magic box.

Set expectations so nobody panics: we are not doing machine learning. No
attention diagrams, no backprop derivations, no transformer architecture
poster. We are going to establish exactly three things: it is a PyTorch class,
it is a pile of numbers, and training means changing the numbers.

That is genuinely enough to make the rest of the module make sense, and it is
the same restraint M2 used with next-token prediction.
-->

---

**Inside the Model · 2/6**

# It's Just a PyTorch Class

```python
"""Any LLM is a PyTorch nn.Module. Nothing more exotic."""

import torch
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("gpt2")

print(isinstance(model, torch.nn.Module))   # True

print(model.transformer.h[0])
# GPT2Block(
#   ln_1: LayerNorm
#   attn: GPT2Attention(c_attn=Conv1D, c_proj=Conv1D)
#   ln_2: LayerNorm
#   mlp:  GPT2MLP(c_fc=Conv1D, c_proj=Conv1D, act=GELU)
# )

n = sum(p.numel() for p in model.parameters())
print(f"{n:,} parameters")       # 124,439,808

# Twelve of those blocks stacked, and that is GPT-2.
# A frontier model is the same block, wider and deeper,
# with a few hundred billion more numbers in it.
```

**What to notice**

- No new framework. It's `nn.Module`.
- You can `print()` it and read the layers
- 124M numbers, and you can count them
- A frontier model is this, wider and deeper

Whatever the marketing says, there is no third thing in there. **Layers and numbers.**

<!--
Run this live. Printing a real model's layer list is the single most
demystifying thing in the module, because the output is boring — and boring is
the point.

What to say while it prints: everything you have used this week, every product
you have read about, is an object like this one. The differences between GPT-2
and a frontier model are the width of the layers, how many are stacked, how
much data went through them, and a lot of engineering around serving. Not the
kind of thing that is in there.

If someone asks about attention: yes, GPT2Attention is in that printout, and
no, we are not opening it today. It is a specific arrangement of the same
matrix multiplies. Point at the reading list and move on — this is the easiest
place in the workshop to lose an hour.
-->

---

**Inside the Model · 3/6**

# The Building Block

```python
"""The whole building block: y = Wx + b."""

import torch
from torch import nn

layer = nn.Linear(in_features=4, out_features=2)

print(layer.weight.shape)   # torch.Size([2, 4])  -> W
print(layer.bias.shape)     # torch.Size([2])     -> b

x = torch.tensor([1.0, 0.0, 2.0, 0.5])

print(layer(x))                       # what a layer does
print(layer.weight @ x + layer.bias)  # ...is exactly this

# Same two numbers, twice. There is no third thing.
#
# Ten learned numbers here. Eight billion in a small
# production model, arranged in a few hundred of these.
# "Training" means: find better values for those numbers.
```

**What to notice**

- `nn.Linear` holds a matrix `W` and a vector `b`
- Calling it *is* `W @ x + b`. Nothing hidden.
- The shapes are the only thing you configure
- Those numbers start random and get better

$$y = f(Wx + b)$$

Every parameter count you've ever read — 8B, 70B, 400B — is the size of these matrices, added up.

<!--
The two print statements returning the same tensor is the whole slide. Show it,
pause, let someone say "wait, that's it?"

The connection worth making explicitly: "8 billion parameters" is not a
capability rating or a difficulty setting. It is literally how many numbers are
in the W and b of every layer summed together. When M2's table said more
parameters means more capability and more cost, this is what was being counted.

Tie back to embeddings from M2 as well. x is a vector of numbers representing
meaning; W transforms it into a different vector in a different space. The
layers are a chain of these transformations, and by the end the vector encodes
"what token comes next".
-->

---

**Inside the Model · 4/6**

# Why Stacking Needs a Kink

```python
"""Two linear layers with nothing between them = one layer."""

import torch
from torch import nn

flat = nn.Sequential(
    nn.Linear(4, 8),
    nn.Linear(8, 2),
)

bent = nn.Sequential(
    nn.Linear(4, 8),
    nn.ReLU(),          # <- the entire difference
    nn.Linear(8, 2),
)

# `flat` gained nothing from being deep. Composing two
# matrix multiplies collapses back into one:
#
#     W2 @ (W1 @ x)  ==  (W2 @ W1) @ x
#
# `bent` cannot be collapsed. ReLU zeroes the negatives,
# and that kink is what lets a stack learn a curve.

x = torch.randn(4)
print(flat(x), bent(x))

# Depth + non-linearity = enough capacity to separate
# "thinking about selling" from "sell 40 shares".
```

**What to notice**

- Two linears with nothing between = one linear
- `W2 @ (W1 @ x)` collapses to `(W2 @ W1) @ x`
- `ReLU` is what makes depth mean something
- Straight lines vs curves — that's the difference

Depth plus non-linearity is where "an advisor is *considering* selling" stops looking like "sell 40 shares".

<!--
The algebra is worth doing on the board if the room is mathematical, and worth
skipping entirely if it is not. The takeaway survives either way: without the
activation function, a deep network is a waste of a deep network.

The analogy that lands: a straight line can separate two clouds of points if
they happen to sit on either side of a line. Language does not sit on either
side of a line. You need something that can bend, and stacking bent pieces is
how you get an arbitrarily complicated boundary.

Do not go further. Nobody needs to know why ReLU beat sigmoid. It is enough
that the non-linearity is there and that it is why depth pays.
-->

---

**Inside the Model · 5/6**

# Training Is Error Reduction

```python
"""Training, entire. Predict, measure error, nudge, repeat."""

import torch
from torch import nn

# A rule we already know: position value = shares x 100
shares = torch.rand(200, 1) * 10
value = shares * 100

model = nn.Linear(1, 1)
loss_fn = nn.MSELoss()
optim = torch.optim.SGD(model.parameters(), lr=0.01)

for step in range(1001):
    predicted = model(shares)          # forward pass
    loss = loss_fn(predicted, value)   # how wrong was it?

    optim.zero_grad()
    loss.backward()                    # which way is down?
    optim.step()                       # one small step

    if step % 250 == 0:
        print(step, round(loss.item(), 3))

print(model.weight.item())    # -> 99.98...

# 0  41883.590   ...   250  0.953   ...   1000  0.001
#
# Nobody told it the rule. It reduced error until it had
# one. A frontier model is this loop, with more numbers.
```

**The four lines that matter**

1. **Forward** — predict with current numbers
2. **Loss** — measure how wrong that was
3. **Backward** — which way is downhill?
4. **Step** — nudge every number that way

Repeat a few trillion times, on a few trillion tokens, and the numbers encode English. **There is no other secret.**

<!--
Run it. Watching the loss fall from 41,883 to 0.001 in four printed lines does
more for intuition than any diagram, because the room can see the model
discover a rule it was never told.

Say the honest scale-up: a real training run is this loop, with a transformer
instead of nn.Linear, next-token prediction instead of MSE, AdamW instead of
SGD, and thousands of GPUs instead of one CPU. The shape does not change. That
is a genuinely useful thing for an engineer to know.

This is also where two later slides get set up, so plant them now: the learning
rate is the size of that nudge (too big and it never settles, too small and it
never arrives), and running this loop too many times on too little data is how
you get memorisation instead of learning.
-->

---

**Inside the Model · 6/6**

# Two Consequences You Can't Argue With

**Knowledge is bounded by the data**

A model cannot know a fact that was never in its optimisation history.

It will still answer. Confidently. That's M2's next-token prediction, unchanged.

**Nobody trains from scratch**

Trillions of tokens, thousands of GPUs, weeks of runtime, millions of dollars.

You'd be paying to re-learn English grammar that somebody already learned.

> So you don't. You download weights that already know language and the world, and you **specialise them**. That's transfer learning, and it's the only reason today is possible on one GPU.

<!--
The left column is M2's hallucination slide with the mechanism now visible.
The model is not lying and not broken. It is producing likely text conditioned
on what it absorbed, and truth was never in the loss function. This is also the
sharpest possible argument for RAG — it is how you get a fact in front of a
model that never saw it.

The right column is the economics. Frontier pre-training runs are eight and
nine figures, and the resulting weights are on HuggingFace for free. Whatever
you think of that, take the gift.

The bridge to say out loud: fine-tuning is not a smaller version of training.
It is the SAME loop, started from weights that already work, run on a tiny
amount of data, for a short time. Everything after this slide is about making
that cheap enough to do on hardware you can actually get.
-->

---

**PEFT · 1/5**

# The VRAM Wall

```python
"""Why you cannot full fine-tune 8B on your laptop."""

PARAMS = 8_000_000_000

weights = PARAMS * 2       # bf16, 2 bytes per number
gradients = PARAMS * 2     # one gradient per weight
optimizer = PARAMS * 8     # Adam keeps 2 fp32 copies

total = weights + gradients + optimizer
print(f"{total / 1e9:.0f} GB before a single activation")
# 96 GB

# Add activations for the backward pass and you are at
# roughly 16x the parameter count.
#
# An H100 has 80 GB. Your laptop has 16.
#
# LoRA deletes lines 2 and 3, not line 1: freeze the
# weights and there are no gradients and no optimizer
# state for 99.8% of them.
```

**Where it all goes**

| Thing | Bytes/param |
|---|---|
| Weights (bf16) | 2 |
| Gradients | 2 |
| Adam optimizer state | 8 |
| Activations | *it depends* |

~**16× the parameter count**. An 8B model wants ~128 GB to full fine-tune. An H100 has 80.

<!--
This slide is why PEFT exists, and doing the arithmetic in front of the room
beats asserting the conclusion. People have heard "you need a big GPU" — they
have not seen that the weights are the SMALLEST part of the bill.

The Adam line surprises everyone. The optimizer keeps a running mean and a
running variance per parameter, both in fp32, which is four times the size of
the bf16 weights. You are paying more to remember how to update the numbers
than to store the numbers.

Then the setup for the next slide: notice that lines 2 and 3 are proportional
to the number of TRAINABLE parameters, not total parameters. Freeze most of the
model and those two lines nearly vanish. That single observation is LoRA.
-->

---

**PEFT · 2/5**

# LoRA: Freeze It, Bolt On a Small Thing

```python
config = LoraConfig(
    r=16,                    # rank: adapter capacity
    lora_alpha=32,           # how loud the adapter is
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],
    task_type="CAUSAL_LM",
)

model = get_peft_model(base, config)
model.print_trainable_parameters()

# trainable: 1,081,344 || all: 495,114,240 || 0.22%
```

**What to notice**

- `W0` is frozen. Never updated, never copied.
- You train `A` and `B` — a thin pair of matrices
- **0.22%** of the parameters are trainable
- The result is a **4 MB file**, not a new model

$$W = W_0 + \frac{\alpha}{r}(B \cdot A)$$

The update a full fine-tune would have made is *low-rank* — it doesn't need `d × k` numbers to express it.

<!--
The intuition to give, in plain words: a full fine-tune computes a giant matrix
of changes to add to the original weights. The LoRA insight is that this change
matrix is far simpler than its size suggests — you can factor it into two thin
matrices and lose almost nothing. So train the factors instead.

The shipping consequence is the part engineers care about and it deserves a
beat: a 4 MB adapter per client, per task, per compliance regime, all sharing
one base model in memory. Swap them at request time. That is an architecture
you cannot build with full fine-tunes.

print_trainable_parameters() is the money line — run it live. 0.22% is the
whole argument, in one number.
-->

---

**PEFT · 3/5**

# The Two Knobs You'll Actually Turn

| Knob | What it is | Start at |
|---|---|---|
| `r` (rank) | Capacity of the adapter. Bigger = more it can learn, more to train. | **16** |
| `alpha` | How loudly the adapter speaks over the base weights. | **32** (= 2r) |
| `target_modules` | Which layers get an adapter. Attention projections first. | `q_proj`, `v_proj` |
| `lora_dropout` | Regularisation. Matters more on small datasets. | **0.05** |

> `r=8` for style and formatting. `r=16–32` for a real task. **`r=64` is almost never the fix** — if it's not learning, your data is wrong.

<!--
Resist tuning theatre. These four values with these four defaults work for the
overwhelming majority of first fine-tunes, and time spent sweeping them is time
not spent fixing the dataset, which is where the actual gains are.

If someone asks what happens when they raise r: more trainable parameters, more
VRAM, more capacity to memorise a small dataset — which is usually a downgrade,
not an upgrade. Capacity is not free.

alpha/r is a scaling factor, so what actually matters is the RATIO, not alpha
alone. Keeping alpha = 2r means changing r doesn't secretly change how strongly
the adapter is applied. That is why the convention exists.

target_modules: adapting only the attention projections is the original paper's
recipe and it is a fine default. Adapting every linear layer costs more and
occasionally helps. Try it second, not first.
-->

---

**PEFT · 4/5**

# QLoRA: Quantise the Frozen Part

```python
"""Load the frozen part in 4 bits. Train adapters in 16."""

import torch
from transformers import AutoModelForCausalLM
from transformers import BitsAndBytesConfig

quant = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",     # NormalFloat4
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=quant,
    device_map="auto",
)

print(model.get_memory_footprint() / 1e9)   # ~5.6 GB
# bf16 would have been ~16 GB, before gradients,
# optimizer state and activations.

# The frozen weights are only ever READ, so 4 bits is
# enough precision. The adapters you actually train
# stay in bf16, because those are the ones learning.
```

**What to notice**

- Base weights load in **4-bit NF4**
- Adapters stay **bf16** — those are learning
- 16 GB → ~5.6 GB, before training even starts
- An 8B fine-tune now fits a 24 GB GPU

The frozen weights are only ever *read*. Precision matters far less on the read path than on the path carrying gradients.

<!--
The one-line summary: LoRA cut the trainable parameters, QLoRA cut the cost of
the ones you are not training. Together they take an 8B fine-tune from a
data-centre job to a single-GPU job, and that is genuinely why this module can
have a lab at all.

NF4 is not plain 4-bit rounding — it is a quantisation designed around the fact
that neural network weights are roughly normally distributed, so the levels are
placed where the weights actually are. That is why the quality loss is small
enough to ignore for most tasks.

Be honest about the trade: 4-bit is not free. On subtle generative tasks you
can measure a small degradation, and if you have the VRAM, bf16 LoRA is still
better. For structured extraction — which is our case — it is undetectable.

Warn them about bitsandbytes on Apple silicon. It wants CUDA. Mac users take
the smaller base model in the lab.
-->

---

**PEFT · 5/5**

# What You Actually Ship

**You do not get a new model**

You get `adapter_model.safetensors` — a few megabytes that sit *on top of* a base model everyone already has.

```
base (5 GB, shared)
  + trades.adapter   (4 MB)
  + compliance.adapter (4 MB)
```

**Which means**

- One base in GPU memory, many adapters
- Swap per request, per client, per region
- Version them like code. They're small.
- Merge into the base only at deploy time

> A fine-tune stops being a scary irreversible event and becomes **a build artefact**.

<!--
This reframe is the most valuable thing in the PEFT section for a senior
engineer, because it changes fine-tuning from a research project into something
that fits in a CI pipeline. Adapters are small, versionable, diffable in the
sense that matters (which dataset and which commit produced them), and cheap to
roll back.

The multi-adapter serving story is real and worth naming: vLLM and friends
support serving many LoRA adapters against one base model. A per-client
adapter, or a per-jurisdiction compliance adapter, is a genuinely practical
architecture rather than a thought experiment.

Merging: you can fold the adapter into the base weights for deployment, which
removes the small inference overhead but gives up the swapping. Decide at
deploy, not at train.
-->

---

<!-- _class: lead -->

**The Dataset · 1/5**

# The dataset is the project.

The training run is an afternoon.

Everyone wants to talk about GPUs.
The work is in the JSONL file.

<!--
Say this before the room has a chance to get comfortable, because the next
fifteen minutes are the least glamorous and most important part of the module.

The proportion, from people who do this for a living: roughly 80% of the effort
is data — collecting, writing, generating, validating, cleaning, splitting.
Maybe 10% is the training run. The rest is evaluation. Nobody's conference talk
reflects this.

The corollary that saves projects: if your fine-tune is not working, the answer
is almost never a hyperparameter. It is your data. More epochs will not rescue
300 inconsistent examples, and neither will a bigger rank.
-->

---

**The Dataset · 2/5**

# The 100–300 Seed Rule

```python
"""One gold example. A domain expert writes 100-300."""

import json

example = {
    "instruction":
        "Extract the trades from this note as JSON.",
    "input":
        "Spoke to Mrs Rao, 12 March. Wants out of TCHR "
        "- sell all 40 shares. Move it into VNGD, about "
        "150 shares if the cash covers it.",
    "output": json.dumps([
        {"symbol": "TCHR", "action": "sell", "shares": 40},
        {"symbol": "VNGD", "action": "buy", "shares": 150},
    ]),
}

with open("data/seeds.jsonl", "a") as f:
    f.write(json.dumps(example) + "\n")

# Write the awkward ones by hand, because the frontier
# model will not invent them for you:
#   - a note with no trade in it at all
#   - tax-loss harvesting across two accounts
#   - a symbol that does not exist
#   - "sell half" (a percentage, not a share count)
```

**What to notice**

- Written by someone who knows the domain
- Messy human input → the exact target output
- JSONL. One example per line. That's the format.
- The edge cases are hand-written on purpose

**Hold out 10% now**, before you generate anything. If your held-out set is synthetic, your score is fiction.

<!--
The number surprises people who expect to need tens of thousands of examples up
front. 100-300 genuinely good ones is the right target for a narrow structured
task, and it is achievable — that is one afternoon with a domain expert and a
spreadsheet, not a data acquisition programme.

Insist on the "someone who knows the domain" part. An engineer guessing at what
an advisor note looks like produces a dataset that teaches the model to parse
fiction. Sit with the advisor. Take their actual notes, with the typos.

The edge cases are where the value concentrates, and the frontier model will
not invent them for you. Notes with no trade at all. Percentages instead of
share counts. Two accounts. A symbol that does not exist. Each one you write by
hand teaches a behaviour that would otherwise be a production incident.

The hold-out warning is not pedantry. Splitting after synthetic expansion leaks
near-duplicates across the split, and you get a 97% score that collapses on
real notes.
-->

---

**The Dataset · 3/5**

# Scale the Seeds With a Frontier Model

```python
def expand(seeds, rounds=1000):
    rows = []
    for _ in range(rounds):
        shown = random.sample(seeds, 3)
        reply = client.messages.create(
            model="claude-opus-5",
            max_tokens=2048,
            temperature=1.0,     # variety in the INPUT
            messages=[{
                "role": "user",
                "content": PROMPT.format(examples=shown),
            }],
        )
        rows += parse_pairs(reply.content[0].text)
    return rows
```

**What to notice**

- 3 real seeds shown per generation call
- `temperature=1.0` — variety in the **input**
- Vary names, dates, typos, missing fields
- The schema stays **rigid**. That's the lesson.

300 seeds → 10–20k rows for a few dollars. You're using an expensive model once to make a cheap model good forever.

<!--
This is the economics that makes small-model fine-tuning practical, and it is
worth naming plainly: you spend maybe $20 of frontier tokens to produce a
dataset that trains a model you run for free.

The prompt design point that matters: high temperature on the NOTE, zero
tolerance on the JSON. You want wild variation in how humans write and none at
all in what comes out. If the generator drifts on schema, tighten the prompt or
constrain the output — do not let the drift into the training set.

Explicitly ask for the ugly cases: incomplete notes, ambiguous ones, notes with
no trade. Left to itself, a frontier model produces 15,000 tidy, well-formed,
suspiciously similar examples, and you will have trained a model that only
works when the input is already clean.

Legal note, real in BFSI: check the provider's terms on using outputs to train
models, and never send real client notes to a frontier API to expand them.
Synthesise from anonymised seeds.
-->

---

**The Dataset · 4/5**

# Then Throw Most of It Away

```python
def keep(row) -> bool:
    try:
        trades = json.loads(row["output"])
    except json.JSONDecodeError:
        return False                     # not even JSON

    for t in trades:
        if set(t) != FIELDS:
            return False                 # wrong schema
        if t["action"] not in ("buy", "sell"):
            return False                 # invented value
        if not isinstance(t["shares"], int):
            return False
    return True


rows = [json.loads(l) for l in open("data/raw.jsonl")]
clean = [r for r in rows if keep(r)]

seen, deduped = set(), []
for r in clean:
    if r["input"] not in seen:
        seen.add(r["input"])
        deduped.append(r)

print(len(rows), len(clean), len(deduped))
# 15000 12841 9702
```

**Three gates, in order**

1. **Parses?** — if it isn't JSON, it's gone
2. **Schema?** — right keys, right types, real values
3. **Duplicate?** — synthetic data collapses fast

`15000 → 12841 → 9702`. Deleting a third of your dataset is a **good** day.

<!--
The instinct to fight here is the sunk-cost one. People paid for those tokens
and want to keep the rows. Every bad row is a lesson you are actively teaching
the model, and a malformed JSON in the training set is a malformed JSON in
production, with interest.

Gate 2 is the one people under-build. Valid JSON with the wrong keys still
parses. Valid JSON with "shares": "forty" still parses. Validate against the
schema you actually want, not against the parser — a Pydantic model here is
strictly better than the hand-rolled check on the slide, and that is a callback
to M0.

Gate 3 is specific to synthetic data and it bites. Generators fall into
attractor states and start producing the same three sentence shapes with
different names. Deduplicate on the input text, and if you want to be thorough,
on embedding similarity — which is the M4 machinery, reused.

Worth saying: read fifty rows yourself. Actually read them. Every dataset
problem I have seen was visible in the first fifty rows and invisible in the
aggregate statistics.
-->

---

**The Dataset · 5/5**

# Learn the Answer, Not the Question

```python
"""Learn the answer, not the question."""

from trl import DataCollatorForCompletionOnlyLM

TEMPLATE = "### Note:\n{input}\n\n### Trades:\n{output}"

collator = DataCollatorForCompletionOnlyLM(
    response_template="### Trades:",
    tokenizer=tokenizer,
)

# Every token BEFORE the response template is labelled
# -100, and the loss function skips it:
#
#   ### Note: Sell 40 TCHR for Mrs Rao
#       -100 -100 -100 -100 -100 -100 -100    (ignored)
#   ### Trades: [{"symbol": "TCHR", ...
#       real labels -> gradients -> learning
#
# Without it, half the capacity goes into learning to
# WRITE advisor notes, which nobody asked for.
#
# This is the most common silent bug in a first
# fine-tune: it trains, the loss falls, and the model
# is quietly worse than it should be.
```

**What to notice**

- Loss is computed on **completion tokens only**
- Everything before the template → labelled `-100`
- `-100` means "skip this one" to the loss function
- Without it, half the capacity learns the wrong job

The most common **silent** bug in a first fine-tune: it trains fine, the loss falls, and the model is quietly worse.

<!--
Silent is the operative word. There is no error, no warning, and the loss curve
looks healthy — it is just that a chunk of what the model learned was how to
generate advisor notes, which is not a product anyone asked for.

The mechanism, plainly: by default the trainer computes loss over every token
in the sequence, so the model is being taught to predict the instruction and
the input as well as the output. The collator relabels the prompt tokens as
-100, PyTorch's cross-entropy ignores that index, and the gradients come only
from the part you care about.

When does it matter most? Long inputs and short outputs — which is exactly our
case, a rambling advisor note in and a compact JSON out. If the prompt is 90%
of the tokens, 90% of your training signal is going to the wrong place.

Chat-template caveat worth mentioning: response_template must match the
tokenised text exactly, and tokenisers sometimes split it differently in
context. If masking silently does nothing, print the labels for one batch and
count the -100s.
-->

---

**Train & Measure · 1/3**

# The Knobs, and Where to Start

```python
args = SFTConfig(
    learning_rate=2e-4,        # 100x the pretraining rate
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    num_train_epochs=3,        # more -> it memorises
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,   # effective batch 16
    bf16=True,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    output_dir="out/trade-parser",
)

trainer = SFTTrainer(
    model=model,               # the PEFT-wrapped model
    args=args,
    train_dataset=train,
    eval_dataset=held_out,
    data_collator=collator,
)
trainer.train()
trainer.save_model()   # -> adapter_model.safetensors
```

**What to notice**

- `2e-4` — far higher than pretraining. Adapters are new.
- 3 epochs. More and it memorises the seeds.
- Small batch × accumulation = effective batch 16
- `load_best_model_at_end` — the last one isn't the best

Twenty lines. The training command was never the hard part.

<!--
The deflation is intentional. After forty minutes of build-up, the actual
training code is a config object and one call, and people should leave knowing
that the difficulty was never here.

Learning rate: 2e-4 is roughly 100x a pretraining rate, and that is correct for
LoRA because the adapter matrices start from scratch (B is zero-initialised) and
have a long way to travel. Do not copy pretraining learning rates.

Gradient accumulation is the trick worth explaining for anyone GPU-poor: run
four small batches, add up the gradients, then step once. Mathematically close
to a batch of 16, but the memory of a batch of 4. This is how you train on the
GPU you actually have.

Epochs: with 10k rows, 3 is plenty. Watch the eval loss rather than trusting the
number — which is the next slide.
-->

---

**Train & Measure · 2/3**

# Watch Two Curves, Not One

**Training loss falling**

Means it is learning *your training set*. That is all it means.

It will keep falling long after the model has stopped getting better.

**Validation loss rising**

Means it started memorising. Every step after that point makes it worse on real inputs.

That's overfitting, and it's the moment to stop.

> Checkpoint every epoch and keep the best one. **The last checkpoint is rarely the best checkpoint** — that's what `load_best_model_at_end` is for.

<!--
The single most common misreading of a training run: "the loss is going down,
it's working". Training loss going down is not evidence of anything except that
gradient descent is functioning.

The picture to draw on the board — two lines, both falling, then the validation
line turns and starts climbing while training keeps dropping. The gap between
them is memorisation. Where they diverge is where you should have stopped.

Symptoms of overfitting a fine-tune, since they will meet these in the lab: the
model reproduces training examples nearly verbatim; it handles inputs shaped
like the seeds and falls apart on anything else; it starts hallucinating symbols
that were common in the training data. Fewer epochs, more data, lower rank —
in that order.

Also worth naming: catastrophic forgetting. Train hard enough on JSON extraction
and the model gets noticeably worse at ordinary conversation. Usually fine — it
has one job — but do not be surprised.
-->

---

**Train & Measure · 3/3**

# Metrics a Compliance Officer Accepts

```python
def score(reply: str, expected: str) -> dict:
    try:
        got = json.loads(reply)
    except json.JSONDecodeError:
        return {"parses": 0, "schema": 0, "exact": 0}

    return {
        "parses": 1,
        "schema": int(all(set(t) == FIELDS for t in got)),
        "exact": int(got == json.loads(expected)),
    }


results = [score(o, t) for o, t in zip(outputs, targets)]

for metric in ("parses", "schema", "exact"):
    hits = sum(r[metric] for r in results)
    print(f"{metric:8} {hits / len(results):.1%}")
```

**Four things worth counting**

- **Parses** — is it JSON at all?
- **Schema** — right keys, right types?
- **Exact match** — correct on the key fields?
- **Disclaimer present** — that's a regex, and it counts

Always score the **base model with a good prompt** on the same set. If it wins, you ship the prompt and go home.

<!--
The baseline comparison is the professional habit and it is the thing most
teams skip. Without it you cannot answer "was this worth six weeks?" — you can
only say the output looks nicer, which is not a finding.

Why these metrics and not an LLM judge: in a regulated workflow the questions
are binary and mechanical. Did it parse. Does it match the schema. Is the
required disclaimer present. Those are cheap, deterministic, reproducible in an
audit, and they do not drift when someone changes the judge's prompt. Save the
judge for the genuinely subjective parts.

The disclaimer regex often gets a laugh, and it should not. "Does every
generated client-facing paragraph contain the required disclosure" is a real
regulatory control, it is testable with a regex, and it belongs in CI.

Land the closing line: the fine-tune is the fourth thing you try, and the eval
is how you find out it was the right one. Which is exactly where this module
started.
-->

---

# 🧪 Lab: Fine-tune a model to read advisor notes (60 min)

Build the whole pipeline on a small model, end to end.

1. Hand-write **30 seed examples** — messy note in, `{symbol, action, shares}` out. Include three that have no trade in them.
2. Score the **base model + a good prompt** on your held-out 10%. Write the number down.
3. Expand the seeds to **~1,500 rows** with the provided generation script.
4. **Filter**: parse → schema → dedupe. Report how many rows you deleted.
5. **QLoRA** a small base model with `r=16`, 3 epochs, prompt loss masked.
6. Score the adapter on the *same* held-out set. Compare to step 2.

Done when: Your `score()` prints parse / schema / exact for both the base model and the adapter, and you can say which one you'd ship

<!--
The step-2-before-step-5 ordering is the point of the lab, not a formality.
Everyone should experience writing down a baseline before training, because
that is the discipline the module is actually teaching.

Expect roughly: base model with a good prompt lands somewhere around 60-75% on
parse and much lower on exact match; the adapter clears 95% on parse and lands
in the 80s on exact. If someone's adapter LOSES to the baseline, that is a
genuinely good outcome for the room — walk through it together. It is almost
always thirty inconsistent seeds, or prompt masking that silently did nothing.

Practicalities: everything runs offline against a small base model committed to
the workshop repo. Step 3's generation calls are pre-run — the expanded dataset
ships with the lab, and the script is there to read, not to execute, because
there are no API keys in the capstone. Mac users: bitsandbytes wants CUDA, so
the fallback is plain LoRA in bf16 on the 0.5B model, which trains in a few
minutes on CPU.

If a group finishes early: have them try r=8 versus r=32 on the same data and
report whether it changed anything. It usually does not, which is the lesson.
-->
