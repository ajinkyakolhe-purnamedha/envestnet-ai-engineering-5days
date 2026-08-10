---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M0 · Python & Its Power in AI

Why this language, and what you can build with it

By the end of this module you can:

- Explain why Python owns AI, and why that is not an accident
- Set up a modern Python project with `uv` in under a minute
- Read and write the six building blocks every AI app is made of
- Pull a real open-source model onto your own laptop

<!--
Set expectations: 90 minutes, roughly half of it hands-on.

This module is deliberately not "Python syntax tutorial". Most of you already
program. What you need is (a) why Python and not the language you already know,
and (b) the specific subset of Python that AI engineering actually uses.
-->

---

# Why Python Won Gen AI

- Reads like English — the code *is* the explanation
- Simplicity is peak genius
- More simplicity → more code → better LLMs at Python → more Python
- The library ecosystem is the real moat

Python is maintainable. In an era where AI writes half your code, **readable beats clever** — by more than it ever did.

<!--
"Simplicity is the ultimate sophistication" — the Apple argument. Simple and
powerful is much harder to build than complicated and powerful.

The feedback loop is the part people miss, and it's an UNINTENDED side effect:
because Python is simple, there is enormously more Python training data on the
internet. So LLMs are measurably better at Python than at any other language.
So people building AI reach for Python. So more Python gets written. It is an
incremental loop that is still compounding — and it means the gap widens, not
narrows.

The maintainability point lands hard with this audience. Zen of Python — we
close the module on it. The discipline of software engineering matters MORE in
the age of AI, not less: you are now reviewing far more code than you write.
-->

---

# The Same Idea, Two Languages

**Python**

```python
"""Chronos: find the positions that are too big."""

holdings = [
    {"symbol": "SPY", "weight": 0.52},
    {"symbol": "QQQ", "weight": 0.31},
    {"symbol": "GLD", "weight": 0.17},
]

for holding in holdings:
    if holding["weight"] > 0.35:
        print(f"Concentrated: {holding['symbol']}")
```

**Java**

```java
// The same intent, in Java.
import java.util.*;

public class Concentration {
  record Holding(String symbol, double weight) {}

  public static void main(String[] args) {
    List<Holding> holdings = List.of(
      new Holding("SPY", 0.52),
      new Holding("QQQ", 0.31),
      new Holding("GLD", 0.17)
    );

    for (Holding holding : holdings) {
      if (holding.weight() > 0.35) {
        System.out.println(
          "Concentrated: " + holding.symbol()
        );
      }
    }
  }
}
```

<!--
This is deliberately GOOD modern Java — records, List.of, no boxing hacks. If
you show bad Java the Java people stop listening and you deserve it. Even at its
best it is twice the lines.

The point is not "Java is bad". It is: to express the same intent, Python asks
you to think about the problem; Java also asks you to think about the machine —
a class you didn't need, a type for every name, a shape declared before use.

Why that matters HERE specifically: in AI work you are experimenting and
throwing away most of what you write. When 90% of your code is discarded, the
cost of ceremony is paid 10× and the benefit is collected once. That ratio is
what makes the trade different for AI than for a long-lived backend service.
-->

---

# Python × Gen AI = Customisable IP

- With Python you can build **any** feature you want
- And you can build it **on top of models you own**
- Download it, customise it, keep it — no vendor sees your data or your edge
- The raw material is free on HuggingFace

> A frontier open-source model costs **~$200M** and a world-class team to train.
> Two countries have managed it. The result is sitting there, downloadable, free.
> Your job is to turn it into a product.

<!--
This is the emotional centre of the whole workshop. Land it properly.

The argument: closed-source APIs give you capability but no ownership. Anyone
can call the same API you're calling. There is no moat in "we call GPT".

Open weights give you something different — you take a $200M artifact for free,
fine-tune it on data only you have, and now you own a competitive advantage
your competitor cannot buy, copy, or even see. They don't know what you did and
can't do anything about it.

That flexibility is the power. Everything in the next 5 days is in service of
this idea.
-->

---

# AI Engineer ≠ AI Researcher

|  | AI Researcher | **AI Engineer** |
|---|---|---|
| Goal | Make a *better model* | Ship a *working feature* |
| Output | Paper, benchmark, weights | Product in production |
| Cares about | Loss curves, architectures, ablations | Latency, cost, evals, failure modes |
| Trains from scratch | Yes | Almost never |
| Headcount needed | Hundreds worldwide | Millions |

Most AI advice online is written for the first column — or by people selling hype. **Both are wrong for you.**

<!--
This slide exists to inoculate them. It is why they get bad advice.

Advice that is correct for a researcher is actively harmful for an engineer:
"you should understand backprop before using an LLM", "train your own model",
"read the transformer paper first". No. You are a software engineer who puts
models into running systems.

Demand asymmetry: the world needs a few thousand AI researchers. It needs
millions of AI engineers. That gap is the career opportunity in this room — and
it is what the rest of this workshop trains.

If someone asks "so should I never learn the theory?" — learn it when a
production problem demands it. Need-driven, not prestige-driven.
-->

---

# Python vs Java/C vs JavaScript

| | Strength | Where it runs | Trade-off |
|---|---|---|---|
| **C / C++ / Java** | Raw throughput | Backend, where the processing happens | Ceremony, slow iteration |
| **JavaScript** | It *is* the browser | Everywhere a user looks | Not performant; backend lives elsewhere |
| **Python** | Simplicity, ecosystem | Increasingly, the default for anything new | Interpreted, line by line — slower |

Python is slower **and that trade is worth it** — because the slow part isn't Python.

- Heavy lifting drops into C / Rust / CUDA underneath (NumPy, PyTorch, Polars)
- `uv`, `ruff`, `polars` — the new generation is Rust with a Python face
- You write the 5% that's logic; the 95% that's math already runs at native speed

<!--
COBOL analogy for the older engineers: mainframes ran on COBOL because that's
where the programs ran. Same logic applies today — languages win by owning a
place, not by being elegant.

The honest caveat: yes, some JavaScript runs on the backend now (Node), and
modern JS tooling is written in Rust. Both are true, both are later
conversations, don't rabbit-hole here.

The key insight to leave them with: when people say "Python is slow", they are
describing the interpreter loop. In AI workloads you spend 99% of wall-clock
inside a matrix multiply that is C or CUDA. Python is the remote control, not
the engine. That's why the trade-off is acceptable and why nearly everything new
starts in Python now.
-->

---

# The Ecosystem

**Tooling** — `uv` for everything

```bash
# One tool: creates the project, pins Python,
# manages every dependency.
uv init chronos
cd chronos

# Pin the interpreter. The whole team now runs
# the identical Python.
uv python pin 3.12

# Add libraries. Resolves + installs in milliseconds.
uv add pandas polars matplotlib
uv add fastapi uvicorn pydantic sqlalchemy
uv add transformers sentence-transformers

# Run inside the project env. No "activate" step.
uv run python app.py
uv run uvicorn app:api --reload
```

**What to notice**

- **Language** — the small core you'll actually use
- **Libraries** — someone already solved it:

| Need | Reach for |
|---|---|
| Excel-scale data | `pandas` |
| Billions of rows | `polars` |
| Graphs | `matplotlib` |
| AI models | `transformers` |
| AI apps | `llama-index`, `langchain`, `pydantic-ai` |

- **IDE** — VS Code or Cursor + Python & Jupyter extensions. Or PyCharm.
- `pip` still works — it's ~10× slower and won't pin your interpreter. Use `uv`. Target Python **3.12** or **3.13**.

<!--
The MATLAB story goes here: MATLAB cost thousands per seat per year. The same
linear algebra, signal processing, and plotting is now free in NumPy/SciPy/
Matplotlib — built by people who then gave it away. That pattern repeated across
statistics (R → pandas), simulation, optimisation. An enormous amount of
formerly-expensive commercial software is now a `uv add` away. That accumulated
gift is what "ecosystem" actually means.

On uv: it replaces pip + venv + pyenv + poetry. One binary, written in Rust.
The "no activate step" thing genuinely surprises people who know Python.

Python version: point them at the official version support table — 3.12/3.13 is
the safe window right now; 3.14 is too new for some AI libraries.
-->

---

**The Python AI Ecosystem · 1/2**

# Libraries, Models, Providers

**Libraries — the tools**

| | |
|---|---|
| `transformers` | Run any open model |
| `diffusers` | Image / video generation |
| `ollama` | Run models locally, easily |
| `vllm` | Serve models fast, at scale |

**Open models — you own these**

| | |
|---|---|
| Qwen | Alibaba |
| GLM | Zhipu |
| Kimi | Moonshot |
| Gemma | Google |
| DeepSeek | DeepSeek |

**Closed models — you rent these**

| | |
|---|---|
| Claude | Anthropic |
| GPT | OpenAI |
| Gemini | Google |

Two columns you download and keep. One column you call and pay for. **That difference is M1.**

<!--
Three shelves in the same shop, and it's worth naming them separately because
people conflate them constantly.

LIBRARIES are the tools, and the split that matters is run-vs-serve:
transformers and ollama are how you run a model on one machine (ollama being
the easy on-ramp — one command, no Python); vllm is how you serve one to many
users with batching and throughput. diffusers is transformers' sibling for
image and video. You will use transformers today.

OPEN MODELS are downloadable weights. Note these are almost all Chinese labs
now — Qwen, GLM, Kimi, DeepSeek — plus Google's Gemma. That is a genuine shift
from two years ago and worth remarking on.

CLOSED MODELS are an API and a bill. Best capability, zero ownership.

The click line is the whole point of the slide, and it sets up M1's four ways.
Do not get drawn into "which is best" — that is M1's closed-vs-open slide.

Licences differ and it is not a footnote: Qwen and DeepSeek are typically
Apache-2.0, Gemma has its own terms. If the pitch is "IP you own", legal will
read the licence.
-->

---

**The Python AI Ecosystem · 2/2**

# Getting One Onto Your Laptop

```python
"""Pull a $200M artifact onto your laptop. For free."""

from huggingface_hub import snapshot_download

snapshot_download(
    # 22M params, ~85 MB on disk
    repo_id="Snowflake/snowflake-arctic-embed-xs",
    local_dir="./models/arctic-embed-xs",
    ignore_patterns=["*.msgpack", "*.h5", "tensorboard*"],
)

# It's now a local folder. No API key. No network.
# No per-token bill. It is yours.
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("./models/arctic-embed-xs")
vectors = model.encode(
    ["broad market index fund", "S&P 500 tracker"]
)

print(vectors.shape)   # (2, 384) -> meaning, as numbers
```

**What to notice**

- Four lines, no API key, no account
- 22M parameters, ~85 MB on disk
- Downloads once, then works with no network
- It is now **a folder you own**
- Size is two different numbers: **parameters** drive quality, **bytes on disk** drive whether you can ship it. M2 comes back to this.

<!--
Run it live if you can. Watching weights land in a local folder is what makes
the "$200M artifact, free" slide two beats ago concrete rather than rhetorical.

The two-numbers point matters and people conflate them: 22M parameters is the
capability number; 85 MB is the logistics number. A model can be small on disk
and still useless, or large on disk and cheap to run. M2's IQ/size/cost table is
where this gets resolved.

This particular model — arctic-embed-xs — is not decoration. It is the
embedding model M2 uses to demonstrate meaning vectors and the one M4's offline
RAG runs on. Say that: the thing they just downloaded gets used twice more.

Demo if time: open huggingface.co, sort by trending, open a model's Files tab so
they see it is just a folder of weights and config.
-->

---

<!-- _class: lead -->

# Building Blocks

The six things every Python AI app is made of

<!--
Shift gears — laptops open from here.

Framing: we're not covering "all of Python". We're covering the specific subset
that shows up in every AI application you will build this week. Six things.
Every snippet is a real file in snippets/m0/ — they can run all of them.
-->

---

**Building Blocks · 1/6**

# Variables & Type Hints

```python
"""Variables and type hints. A Chronos price row."""

# Python infers types. You never declare them to run code.
symbol = "SPY"
close = 323.54
is_tradable = True
tags = ["equity", "index", "large-cap"]

# But you SHOULD annotate. Hints are documentation the
# IDE can check -- and what Pydantic/FastAPI use to
# validate at runtime.
shares: float = 100.0
cash_balance: float = 25_000.00
sectors: list[str] = ["Broad Market", "Technology"]
dividend: float | None = None      # may be absent

print(f"{symbol} - {close:,.2f} x {shares:g} shares")
```

**What to notice**

- No type declarations needed to run
- But annotate anyway — `list[str]`, `float | None`
- Hints are checked by your IDE, not the interpreter
- **This is the bit that matters:** Pydantic and FastAPI read these hints and turn them into real runtime validation
- Type hints are how a "dynamic" language gets a static contract — without giving up the fast iteration.

<!--
The `float | None` syntax (3.10+) is worth pausing on — it replaces
Optional[float] and reads better.

Do NOT let this become a static-vs-dynamic-typing debate. The pragmatic answer:
annotate function signatures and data models, skip annotations on obvious local
variables. That's what the ecosystem actually does.

The Pydantic connection is the payoff — it lands two slides from now. Plant it
here so it doesn't feel like magic later.
-->

---

**Building Blocks · 2/6**

# Functions & Logging

```python
"""Functions and logging. Never print() in real code."""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
)
log = logging.getLogger("chronos.portfolio")


def position_value(shares: float, close: float) -> float:
    """What one holding is worth. Raises on bad input."""
    if shares < 0 or close <= 0:
        raise ValueError(f"bad position: {shares} @ {close}")

    value = round(shares * close, 2)
    log.info("value: %g x %.2f -> %.2f", shares, close, value)
    return value


if __name__ == "__main__":
    position_value(100, 323.54)
```

**What to notice**

- Docstring first — it's what an LLM reads too
- Annotated signature: `(float, float) -> float`
- Fail loudly and early on bad input
- `logging`, never `print`
- **Why logging matters more with AI:** model output is non-deterministic. When a feature misbehaves in production, the log is the *only* record of what the model actually saw and said.

<!--
The print-vs-logging point usually gets nods but no real conviction until you
frame it the AI way: with deterministic code you can reproduce a bug locally.
With an LLM in the loop you often cannot — same prompt, different output. Your
logs are the only forensic evidence you will ever have. Log the prompt, log the
response, log the model version.

The `%s` lazy-formatting style in log calls (not f-strings) is deliberate —
the string is only built if that level is enabled. Small thing, mention it if
the room is sharp.
-->

---

**Building Blocks · 3/6**

# Classes

```python
@dataclass
class Holding:
    """A position in one symbol. Data, so: dataclass."""

    symbol: str
    shares: float
    average_cost: float
    close: float
    sectors: list[str] = field(default_factory=list)

    @property
    def market_value(self) -> float:
        return self.shares * self.close


class Portfolio:
    """Behaviour + protected state, so: plain class."""

    def __init__(self, cash: float) -> None:
        self._cash = cash
        self._holdings: list[Holding] = []

    def add(self, holding: Holding) -> None:
        self._holdings.append(holding)

    @property
    def total_value(self) -> float:
        held = sum(h.market_value for h in self._holdings)
        return self._cash + held
```

**What to notice**

- `@dataclass` — the shape of your data, no boilerplate
- `field(default_factory=list)` — mutable defaults need this
- `@property` — computed, accessed like an attribute
- Plain `class` when there's behaviour and state to protect
- Rule of thumb: **dataclass for data, class for behaviour.** Pydantic's `BaseModel` is the same idea plus validation — next slide.

<!--
The mutable-default trap is the classic Python footgun. Worth 30 seconds:
`def f(x, items=[])` shares that list across every call. dataclasses refuse to
let you do it, which is why default_factory exists.

Don't teach inheritance here. In AI application code you compose far more than
you inherit, and the deep hierarchy instinct from Java is actively unhelpful.
-->

---

**Building Blocks · 4/6**

# Data: CSV → Insight

```python
"""Reading and processing data.

pandas for thousands of rows.
"""

import pandas as pd

prices = pd.read_csv("data/sample_prices.csv")

# Filter, group, aggregate. Three chained operations
# replace the nested loop you'd write elsewhere.
summary = (
    prices[prices["date"] >= "2020-03-01"]
    .groupby("symbol")["close"]
    .agg(["count", "mean", "max"])
    .sort_values("mean", ascending=False)
)

print(summary)

# Billions of rows? Change the import, keep the logic:
#   import polars as pl
#   prices = pl.scan_csv("data/sample_prices.csv")
```

**What to notice**

- `read_csv` → three chained operations → answer
- The nested loop you'd write elsewhere is gone
- Same logic, billions of rows? Swap `pandas` → `polars`
- **Where this hits AI:** every RAG pipeline, every eval run, every fine-tuning dataset starts as a dataframe. You'll use this on Day 2.

<!--
Prices CSV is deliberately the Chronos data — the same file is what the lab
reads in Exercise 1 and what the market-data pipeline loads into SQLite.
Continuity is the point.

Polars: lazy + out-of-core + multithreaded, written in Rust. Mention that the
API is deliberately similar so switching is cheap, but don't teach it now.
-->

---

**Building Blocks · 5/6**

# Databases

```python
"""Database read/write. sqlite3 ships with Python."""

import sqlite3

conn = sqlite3.connect("chronos.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        symbol TEXT NOT NULL,
        date   TEXT NOT NULL,
        close  REAL NOT NULL,
        PRIMARY KEY (symbol, date))
""")

# Write: always parameterised. Never f-string SQL.
conn.executemany(
    "INSERT OR REPLACE INTO prices VALUES (?, ?, ?)",
    [
        ("SPY", "2020-03-12", 248.11),
        ("SPY", "2020-03-13", 269.32),
    ],
)
conn.commit()
# Read: the last close on or BEFORE a date. Never a
# price the investor's simulated date hasn't reached.
rows = conn.execute(
    "SELECT date, close FROM prices"
    " WHERE symbol = ? AND date <= ?"
    " ORDER BY date DESC LIMIT 1",
    ("SPY", "2020-03-14"),
)
print(list(rows))
conn.close()
```

**What to notice**

- `sqlite3` ships with Python — nothing to install
- Parameterised queries: `?`, never f-strings
- `executemany` for bulk writes
- Same patterns scale to Postgres via SQLAlchemy
- On Day 2 this table gets a sibling: a **vector** database, storing meaning instead of values.

<!--
The SQL injection point is non-negotiable and takes ten seconds. Say it once,
firmly: if you are building a query with an f-string you have written a
vulnerability. Doubly true when the string came from an LLM.

The vector-DB forward reference is deliberate — it makes M4 feel like a natural
extension rather than a new universe.
-->

---

**Building Blocks · 6/6**

# The API Server

```python
class Holding(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    shares: float = Field(gt=0)         # rejected at the edge
    average_cost: float = Field(gt=0)
    risk_level: str = "MEDIUM"


BOOK: dict[str, Holding] = {}


@api.post("/holdings")
def add_holding(holding: Holding) -> Holding:
    """Pydantic already validated it. Nothing to check."""
    BOOK[holding.symbol] = holding
    return holding


@api.get("/holdings/{symbol}")
def get_holding(symbol: str) -> Holding:
    if symbol not in BOOK:
        raise HTTPException(404, f"no holding {symbol}")
    return BOOK[symbol]
```

**What to notice**

- `BaseModel` + type hints = automatic validation
- `Field(gt=0)`, `Field(ge=0, le=5)` — constraints as declarations
- Bad requests are rejected **at the edge**, never in your handler
- Free interactive docs at `/docs`
- This is the payoff for annotating types. Same hints, three jobs: **IDE checking, runtime validation, API contract.**

<!--
Run this live if at all possible. `uv run uvicorn api_server:api --reload`, open
localhost:8000/docs, POST an item with price -5, watch Pydantic reject it with a
precise error you did not write. That moment sells type hints better than any
slide.

Forward reference: in M3 this same server grows an LLM-backed endpoint. The
Pydantic model becomes the *structured output schema* the model must fill —
which is how you stop an LLM returning free-form prose. Plant it now.
-->

---

# Running & Debugging

**Ways to run**

```bash
uv run python app.py             # a script
uv run uvicorn app:api --reload  # a server
uv run pytest                    # tests
```

**When it breaks**

```bash
uv run pytest -x --pdb    # stop and drop into a debugger
```

**What to notice**

- Breakpoint in VS Code — click the gutter, F5
- `breakpoint()` anywhere in the code
- Read the traceback **bottom-up**: the last line is what broke, above it is how you got there
- Reading tracebacks bottom-up is the single highest-leverage habit here. Most people read top-down and give up.

<!--
Keep this brisk — it's plumbing, and they'll pick it up in the lab anyway.

Traceback direction is the one thing worth insisting on. The last line is what
actually broke; everything above it is the path that got you there. Newcomers
read from the top, hit framework internals they don't recognise, and conclude
the error is unreadable.

`uv run` matters more than it looks: it means nobody has to remember to
activate a virtualenv, which removes the single most common "it works on my
machine" failure in a room of thirty laptops.

The explore-vs-ship progression (python → ipython → jupyter) is now its own
slide after the lab.
-->

---

# Code You'll Still Understand in Six Months

**Before**

```python
# proc.py
def proc(d, f=0):
    r = []
    for x in d:
        if x["w"] > 0.35 and (not f or x["s"] == f):
            r.append(x)
    return r
```

**After**

```python
# portfolio/concentration.py
def concentrated(holdings: list[Holding],
                 sector: str | None = None) -> list[Holding]:
    """Positions over 35% of the book, in one sector."""
    return [
        holding for holding in holdings
        if holding.weight > 0.35
        and (sector is None or holding.sector == sector)
    ]
```

**What changed**

- `proc` → `concentrated` — the name *is* the docstring
- `d`, `f`, `r`, `x` → words a reader knows
- `x["w"] > 0.35` → `holding.weight > 0.35`
- `proc.py` → `portfolio/concentration.py`
- One job per function, one job per file
- Same behaviour, same line count. The second one you can hand to someone else — **or to a model.**

<!--
Both versions work. That is the point — this is not about correctness, and if
you frame it as "the left one is a bug" the argument collapses.

The four moves, in order of payoff:
  1. Name things what they are. A good function name removes the need for a
     comment and often for the docstring too.
  2. No single-letter names outside a genuine loop index or a maths formula.
  3. Small functions. If you cannot name it in two words, it does two things.
  4. File and folder names are part of the API. proc.py tells a reader nothing;
     portfolio/concentration.py tells them where to look next.

WHY THIS MATTERS MORE NOW, and this is the AI-specific argument — make it
explicitly, it is the reason this slide exists in an AI course:

You are about to start generating a lot of code. Two consequences. First, you
will review far more code than you write, and clear naming is what makes review
possible at speed. Second, the model reads your codebase as context — good
names, small functions and honest file paths are what let it find the right
place to change. Sloppy structure degrades the model's output, not just yours.

Callback: this is the Zen of Python slide arriving early, and we close the
module on it.
-->

---

# 🧪 Lab: Market data, point-in-time prices, a benchmark (70 min)

<code>labs/python_basics/python_basics_lab.py</code> — fill in three functions.

1. **Read closes from a CSV** *(12 min)* — market data arrives as files first
2. **The price on or before a date** *(18 min)* — never a price the investor hasn't reached
3. **Compare the account to a benchmark** *(30 min)* — **ships to the app**

Done when: <code>uv run pytest tests/labs -m lab</code> is green, and a buy-and-hold line appears on the account value chart.

Prerequisite: <code>uv run python -m scripts.load_market_data</code> · Stretch: measure the worst drawdown

<!--
Circulate. The two failure modes you'll see: (1) forgetting `uv run` and hitting
the system Python, (2) running from the wrong directory, so the CSV path misses.

Exercise 2 is the one to make a point of. "The latest close on or BEFORE this
date" is not a Python trick — it is the rule the entire application obeys, and
the reason the app can never show a price from the investor's future. Weekends
fall out of it for free: a Saturday values from Friday's close.

Exercise 3 is why the lab is worth 70 minutes. They are not writing a toy — the
function graduates into `chronos/portfolio/benchmark_comparison.py` and the line
appears on the chart. Show that happening at the front of the room when the
first person passes.

Unfinished exercises report "not started yet" and the rest still run, so nobody
is blocked. `labs/solutions/` has a working version of everything — say it
exists, and say a hint they worked out is worth more than a solution they read.

Tell them explicitly: keep this repo. M1 and M2 add a model to it, M4 adds RAG
over the investing corpus, M7 makes it agentic. Everything compounds from here.
-->

---

# Python → IPython → Jupyter

**The Java/C loop**

Write it all → compile → test → *hope*

You commit to the design before you see it run.

```bash
uv run python       # bare REPL
uv run ipython      # + history, %timeit
uv run jupyter lab  # + cells and plots
```

**The Python loop**

Write a line → **look at it** → change it

Python is glue code. You write it *on the way* to making it work — run it, read the output, learn something, adjust.

That's not sloppiness. It's the same loop a data analyst uses, and it's why the language ended up owning analytics **and** AI.

> Notebooks are for *exploring*. Modules are for *shipping*.
> Prototype in Jupyter, then move the code into `.py` files.

<!--
This slide is about a working style, not about three commands. The commands are
the least interesting thing on it.

The contrast to draw: in Java or C the loop is expensive — compile, wait, run —
so you think hard up front and commit to a design before you see it execute.
Python's loop is nearly free, so you find the design by running things. Neither
is better in the abstract; they suit different problems.

For AI work the fast loop is decisive, because you genuinely cannot predict what
a model will do with your data. You have to look. That is why every AI tutorial
you will ever see is a notebook.

IPython is worth 60 seconds live: tab-completion on a dataframe, `?` for a
docstring, `%timeit` on a slow line. It is the same REPL with the ergonomics
filled in, and most engineers who "know Python" have never used it.

Then the caveat, and say it plainly because they are about to inherit a lot of
notebook-shaped advice: notebooks have hidden execution-order state, no tests,
no imports, and they do not diff in git. Explore in Jupyter, ship in modules.
That's the same discipline as the naming slide, applied to file format.
-->

---

<!-- _class: lead -->

# The Zen of Python

Beautiful is better than ugly.
**Explicit is better than implicit.**
Simple is better than complex.
**Readability counts.**
There should be one — and preferably only one — obvious way to do it.

`python -c "import this"`

<!--
Close the loop on the module's opening claim.

The closing argument, and it's the one that carries into the next five days:
these principles were always good advice. You are now reviewing far more code than you write, most of it
generated. Explicit, simple, readable code is code you can actually review.
Clever code is code you will approve without understanding.

Software engineering discipline didn't get less important when AI started
writing code. It got to be the only thing standing between you and a codebase
nobody understands.

Bridge to M1: "You now have the language. Next: the models."
-->
