---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M0.0.1 · Python & Its Power in AI

Why this language, and what you can build with it

By the end of this module you can:

- Explain why Python is the default for AI application work
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

# M0.1.1 · Why Python Is The Default

- Low ceremony — the code stays close to the business rule
- Fast iteration — useful when most experiments are thrown away
- Large public codebase — LLMs are generally strong at Python
- Library depth — the ecosystem is the real advantage

Python is maintainable. When AI generates more code than you write by hand, **readable beats clever**.

<!--
Python is useful here for practical reasons, not because it is elegant in the
abstract. AI application code is mostly orchestration: load data, call a model,
validate the result, call a tool, store state, expose an API, and log what
happened. Python expresses that coordination layer with little ceremony.

The LLM feedback loop is also practical. There is a large amount of public
Python code, so coding models tend to perform well on Python. That makes Python
a good default for AI-assisted development, especially when combined with clear
names and small files.

The maintainability point matters throughout the week. Students will review
generated code, not just write code. Readable code is code they can inspect,
test, and correct.
-->

---

# M0.1.2 · The Same Idea, Two Languages

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

Full running version: `SLIDES-markdown/m0/readable.py`

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
This is deliberately good modern Java — records, `List.of`, no artificial
boilerplate. The comparison should be fair: even good Java uses more ceremony
for this small rule.

The point is not "Java is bad". It is: to express the same intent, Python asks
you to think about the problem; Java also asks you to think about the machine —
a class you didn't need, a type for every name, a shape declared before use.

Why that matters HERE specifically: in AI work you are experimenting and
throwing away most of what you write. When 90% of your code is discarded, the
cost of ceremony is paid 10× and the benefit is collected once. That ratio is
what makes the trade different for AI than for a long-lived backend service.
-->

---

# M0.1.3 · Python × Gen AI = Customisable IP

- Python is the application layer around the model
- Open weights can be downloaded, customized, and kept
- Private data can stay inside your boundary
- The raw material is free on HuggingFace

Open weights change the ownership model:

```text
closed API  -> rent capability
open model  -> own the artifact, adapt it, serve it yourself
```

<!--
The argument is about ownership, not ideology. Closed APIs give fast access to
strong capability, but the same endpoint is available to competitors. The
application value comes from product design, proprietary data, workflow
integration, evaluation, and operational reliability.

Open weights add another option: the model artifact can live inside your own
system. You can fine-tune it, quantize it, evaluate it, and serve it under your
constraints. That does not automatically make it better than a closed model; it
changes what you can control.

M1 turns this into a model-selection decision. M6 returns to it when
fine-tuning changes a model's behavior for a narrow task.
-->

---

# M0.1.4 · AI Engineer ≠ AI Researcher

|  | AI Researcher | **AI Engineer** |
|---|---|---|
| Goal | Make a *better model* | Ship a *working feature* |
| Output | Paper, benchmark, weights | Product in production |
| Cares about | Loss curves, architectures, ablations | Latency, cost, evals, failure modes |
| Trains from scratch | Yes | Almost never |
| Headcount needed | Hundreds worldwide | Millions |

Most AI application teams live in the second column.

<!--
This slide separates two jobs that are often mixed together. Researchers improve
models. Engineers build reliable systems around models. The skills overlap, but
the success criteria are different.

Advice that is correct for a researcher can be the wrong starting point for an
engineer. Training from scratch, architecture research, and benchmark chasing
are not the normal path to a useful enterprise feature. The normal path is to
choose an existing model, wrap it in software, measure it, and control its
failure modes.

Demand asymmetry: the world needs a few thousand AI researchers. It needs
millions of AI engineers. That gap is the career opportunity in this room — and
it is what the rest of this workshop trains.

Theory is still useful. The ordering matters: learn deeper internals when a
production decision requires them. M2 gives enough model mechanics to make
engineering decisions without turning the course into a research seminar.
-->

---

# M0.1.5 · Python vs Java/C vs JavaScript

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

The caveat: some JavaScript runs on the backend now, and modern JS tooling is
often written in Rust. Both are true, but they are not the decision this slide
is teaching.

The key insight to leave them with: when people say "Python is slow", they are
describing the interpreter loop. In AI workloads you spend 99% of wall-clock
inside a matrix multiply that is C or CUDA. Python is the remote control, not
the engine. That's why the trade-off is acceptable and why nearly everything new
starts in Python now.
-->

---

# M0.2.1 · The Ecosystem

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

**The Python AI Ecosystem · 1 of 2**

# M0.2.2 · Libraries, Models, Providers

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
| GPT | OpenAI |
| Gemini | Google |
| Command | Cohere |

Two columns you download and keep. One column you call and pay for.

That difference is M1.

<!--
There are three different categories here, and mixing them leads to confused
architecture decisions.

Libraries are tools. `transformers` and `ollama` run models locally. `vllm`
serves models with batching and throughput. `diffusers` handles image and video
generation. These are not models; they are software used to run models.

Open models are downloadable weights. Closed models are accessed through APIs.
The operational questions are different: where the data goes, who pays for
tokens, who controls serving, and whether the artifact can be customized.

This slide sets up M1's four model-access patterns. Do not turn it into a
ranking discussion yet.

Licences differ and it is not a footnote: Qwen and DeepSeek are typically
Apache-2.0, Gemma has its own terms. If the pitch is "IP you own", legal will
read the licence.
-->

---

**The Python AI Ecosystem · 2 of 2**

# M0.2.3 · Getting One Onto Your Laptop

```python
"""Pull a $200M artifact onto your laptop. For free."""

# Run once with network, then the weights live in a
# folder you own. For this workshop, that already
# happened: OFFLINE-AI-Models/ is in the repo.

from chronos_offline import generate

reply = generate(
    "In one sentence: what is a concentrated portfolio?",
    max_new_tokens=40,
)
print(reply)
```

Full running version: `SLIDES-markdown/m0/offline_model.py`

**What to notice**

- No API key, no account
- No network after the weights are present
- No per-token bill
- A local artifact you can inspect, serve, or fine-tune
- 22M parameters, ~85 MB on disk
- Downloads once, then works with no network
- It is now a local artifact you control
- Size is two different numbers: **parameters** drive quality, **bytes on disk** drive whether you can ship it. M2 comes back to this.

<!--
Run it live if time allows. Seeing a model become a local folder makes the
ownership point concrete.

The two-numbers point matters and people conflate them: 22M parameters is the
capability number; 85 MB is the logistics number. A model can be small on disk
and still useless, or large on disk and cheap to run. M2's IQ/size/cost table is
where this gets resolved.

This particular model — arctic-embed-xs — is not decoration. It is the
embedding model M2 uses to demonstrate meaning vectors and the one M4's offline
RAG runs on. Say that: the thing they just downloaded gets used twice more.

Demo if time: open a model's Files tab on HuggingFace. The useful observation is
that a model is files: weights, tokenizer, config, and metadata.
-->

---

<!-- _class: lead -->

# M0.3.1 · Building Blocks

The six things every Python AI app is made of

<!--
Shift gears — laptops open from here.

Framing: we're not covering "all of Python". We're covering the specific subset
that shows up in every AI application you will build this week. Six things.
Every snippet is a real file in `SLIDES-markdown/m0/` — they can run all of
them with `uv run --project ../CODE-ALONGS python m0/<file>.py`.
-->

---

**Building Blocks · 1 of 6**

# M0.3.2 · Variables & Type Hints

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

Full running version: `SLIDES-markdown/m0/variables.py`

**What to notice**

- No type declarations needed to run
- But annotate anyway — `list[str]`, `float | None`
- Hints are checked by your IDE, not the interpreter
- Pydantic and FastAPI read these hints and turn them into runtime validation
- Type hints are how a "dynamic" language gets a static contract — without giving up the fast iteration.

<!--
The `float | None` syntax (3.10+) is worth pausing on — it replaces
Optional[float] and reads better.

Do NOT let this become a static-vs-dynamic-typing debate. The pragmatic answer:
annotate function signatures and data models, skip annotations on obvious local
variables. That's what the ecosystem actually does.

The Pydantic connection arrives two slides from now. Introduce it here so the
runtime-validation behavior does not feel like magic later.
-->

---

**Building Blocks · 2 of 6**

# M0.3.3 · Functions & Logging

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

Full running version: `SLIDES-markdown/m0/functions.py`

**What to notice**

- Docstring first — it's what an LLM reads too
- Annotated signature: `(float, float) -> float`
- Fail loudly and early on bad input
- `logging`, never `print`
- With non-deterministic model output, logs are the record of what the model saw and returned

<!--
With deterministic code, a failure is often reproducible locally. With a model
in the loop, the same prompt may not produce the same text. Logs record the
prompt, response, model version, tool calls, and decisions made around them.

The `%s` lazy-formatting style in log calls (not f-strings) is deliberate: the
string is only built if that level is enabled.
-->

---

**Building Blocks · 3 of 6**

# M0.3.4 · Classes

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

Full running version: `SLIDES-markdown/m0/classes.py`

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

**Building Blocks · 4 of 6**

# M0.3.5 · Data: CSV → Insight

```python
"""Reading and processing data.

pandas for thousands of rows.
"""

import pandas as pd

prices = pd.read_csv("data/prices.csv")

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
#   prices = pl.scan_csv("data/prices.csv")
```

Full running version: `SLIDES-markdown/m0/data_csv.py`

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

**Building Blocks · 5 of 6**

# M0.3.6 · Databases

```python
"""Database read/write. sqlite3 ships with Python."""

import sqlite3

conn = sqlite3.connect(":memory:")
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
        ("AAPL", "2020-05-29", 79.49),
        ("AAPL", "2020-06-01", 80.46),
        ("AAPL", "2020-06-02", 80.83),
    ],
)
conn.commit()
# Read: the last close on or BEFORE a date. Never a
# price the investor's simulated date hasn't reached.
rows = conn.execute(
    "SELECT date, close FROM prices"
    " WHERE symbol = ? AND date <= ?"
    " ORDER BY date DESC LIMIT 1",
    ("AAPL", "2020-06-01"),
)
print(list(rows))
conn.close()
```

Full running version: `SLIDES-markdown/m0/database.py`

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

**Building Blocks · 6 of 6**

# M0.3.7 · The API Server

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

Full running version: `SLIDES-markdown/m0/api_server.py`

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

# M0.4.1 · Running & Debugging

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
- Read tracebacks bottom-up: exception first, call path second

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

# M0.4.2 · Code You'll Still Understand in Six Months

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

Full running version: `SLIDES-markdown/m0/naming.py`

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

# M0.L1 · Lab: Market Data, Point-In-Time Prices, Benchmark

`labs/python_basics/python_basics_lab.py` — fill in three functions.

1. **Read closes from a CSV** *(12 min)* — market data arrives as files first
2. **The price on or before a date** *(18 min)* — never a price the investor hasn't reached
3. **Compare the account to a benchmark** *(30 min)* — **ships to the app**

Done when: `uv run pytest tests/labs -m lab` is green, and a buy-and-hold line appears on the account value chart.

Prerequisite: `uv run python -m scripts.load_market_data`

Stretch: measure the worst drawdown.

<!--
Common failure modes: (1) forgetting `uv run` and hitting
the system Python, (2) running from the wrong directory, so the CSV path misses.

Exercise 2 is the one to make a point of. "The latest close on or BEFORE this
date" is not a Python trick — it is the rule the entire application obeys, and
the reason the app can never show a price from the investor's future. Weekends
fall out of it for free: a Saturday values from Friday's close.

Exercise 3 is the capstone connection. They are not writing a toy — the
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

# M0.4.3 · Python → IPython → Jupyter

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

# M0.5.1 · The Zen of Python

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
