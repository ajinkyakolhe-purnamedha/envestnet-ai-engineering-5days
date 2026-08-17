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
- Compare a local model with a hosted API call
- Build, run, test, and debug a small Python wealth application

<!--
**Instructor only:** Plan for 90 minutes of instruction and guided code-alongs,
followed by an optional 20-minute mini lab or a separate 1–2 hour main lab.

This module is deliberately not "Python syntax tutorial". Most of you already
program. What you need is (a) why Python and not the language you already know,
and (b) the specific subset of Python that AI engineering actually uses.
-->

---

# M0.1.1 · Why Python Is The Default

- **Reads close to English** — simpler to read, understand, and write when you are exploring an idea.
- **Deep ecosystem** — because Python is accessible, people have built libraries for data, models, APIs, evaluation, and deployment.
  - Library depth—not syntax alone—is the practical advantage.
- **Maintainable code** — when AI generates more code than you write by hand, readable beats clever.
- **Strong default for AI-assisted development** — coding models see a large amount of public Python, and clear Python is easy to inspect and correct.
- **AI customization ecosystem** — Python is not only backend glue; it is where data pipelines, model SDKs, local models, and AI features meet.

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
cash = 100_000
shares = 10
historical_price = 80.50

cost = shares * historical_price
cash_left = cash - cost

print("Cost:", cost)
print("Cash left:", cash_left)
```

Snippet and code-along: `CODEALONGS/day_1/m0_section_1_share_purchase/01_purchase_cost.py` → `02_purchase_cost_code_along.ipynb`

**Java**

```java
public class PurchaseCost {
  public static void main(String[] args) {
    double cash = 100_000;
    int shares = 10;
    double historicalPrice = 80.50;

    double cost = shares * historicalPrice;
    double cashLeft = cash - cost;

    System.out.println("Cost: " + cost);
    System.out.println("Cash left: " + cashLeft);
  }
}
```

<!--
This is deliberately ordinary modern Java. The comparison should be fair: both
versions calculate the same purchase cost and cash remaining.

The point is not "Java is bad". It is: to express the same intent, Python asks
you to think about the problem; Java also needs a class and an entry-point
method before it can run the same small calculation.

Why that matters HERE specifically: in AI work you are experimenting and
throwing away most of what you write. When 90% of your code is discarded, the
cost of ceremony is paid 10× and the benefit is collected once. That ratio is
what makes the trade different for AI than for a long-lived backend service.
-->

---

# M0.1.3 · Python × Gen AI = Customisable IP

- Python builds the ordinary business logic of an application: rules, data flow, APIs, and user workflows.
- Add AI features to that same application through a hosted-model SDK such as Gemini, OpenAI, or Anthropic.
- Or use open weights when local control, customization, or data boundaries matter.
  - Open weights are not automatically better; they give you a different operating model.

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
| Typical focus | Model innovation | Product and system delivery |

Most AI application teams live in the second column: they choose an existing
model, make it useful in a workflow, and operate it reliably.

<!--
This slide separates two jobs that are often mixed together. Researchers improve
models. Engineers build reliable systems around models. The skills overlap, but
the success criteria are different.

Advice that is correct for a researcher can be the wrong starting point for an
engineer. Training from scratch, architecture research, and benchmark chasing
are not the normal path to a useful enterprise feature. The normal path is to
choose an existing model, wrap it in software, measure it, and control its
failure modes.

The point is not a headcount comparison. Most product teams need engineers who
can turn an existing model into a reliable, useful feature; that is what the
rest of this workshop trains.

Theory is still useful. The ordering matters: learn deeper internals when a
production decision requires them. M2 gives enough model mechanics to make
engineering decisions without turning the course into a research seminar.
-->

---

# M0.1.5 · Python vs Java/C vs JavaScript

| | Strength | Where it runs | Trade-off |
|---|---|---|---|
| **C / C++ / Java** | Raw throughput | Backend, where the processing happens | Ceremony, slow iteration |
| **JavaScript / TypeScript** | Browser and web tooling | Browser and backend services | Different AI/data ecosystem; runtime trade-offs vary |
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

Create a project once; then install the one library your feature needs:

```bash
uv init wealth-demo
cd wealth-demo

uv add transformers torch       # run a local model
uv add google-genai             # call Gemini
uv add python-dotenv            # load secrets from .env
uv add fastapi uvicorn          # run a local API server
uv add openai anthropic boto3   # other hosted providers
```

`uv` records the dependency and gives every participant the same environment.

- It creates the project, manages the virtual environment, and records the dependency versions.
- `uv run ...` uses that project environment without asking participants to activate anything first.
- Add the library for the feature you are building; do not install every library in the list.

Code card: `CODEALONGS/day_1/m0_section_2_model_access/01_install_packages.sh`

<!--
`uv init` creates the project metadata. Each `uv add` records a dependency in
`pyproject.toml` and resolves an environment for that project. The lock file is
what lets a teammate reproduce the same dependency set later.

The package lines are alternatives, not a checklist to install all at once.
Choose the line that matches the feature: a local model, a hosted model call, a
web API, or another provider integration. `uv run` then runs a command inside
that project environment without activating a virtual environment manually.
-->

# M0.2.2 · Libraries, Models, Providers


**Closed models — you rent these**

| | |
|---|---|
| GPT | OpenAI |
| Gemini | Google |
| Command | Cohere |

**Libraries — the tools**

| | |
|---|---|
| `transformers` | Run any open model |
| `diffusers` | Image / video generation |
| `ollama` | Run models locally, easily |

**Open models — you own these**

| | |
|---|---|
| Qwen | Alibaba |
| GLM | Zhipu |
| Kimi | Moonshot |
| Gemma | Google |
| DeepSeek | DeepSeek |


The three categories answer different questions:

- **Libraries** are tools you install to run or build things.
- **Open models** are downloadable artifacts you can keep and serve.
- **Closed models** are provider APIs you call and pay for.

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

The categories are not a ranking. They answer different design questions and
set up M1's model-access patterns.

Licences differ and it is not a footnote: Qwen and DeepSeek are typically
Apache-2.0, Gemma has its own terms. If the pitch is "IP you own", legal will
read the licence.
-->

---

**The Python AI Ecosystem · 2 of 2**
# M0.2.3 · Getting One Onto Your Laptop

```python
from transformers import pipeline

model_path = "OFFLINE-AI-Models/smollm2-135m-instruct"
generate = pipeline("text-generation", model=model_path)

answer = generate("Say hello.", max_new_tokens=20, do_sample=False)
print(answer[0]["generated_text"])
```

Full running version: `CODEALONGS/day_1/m0_section_2_model_access/02_huggingface_offline.py`

**What to notice**

- No API key, no account
- No network after the weights are present
- No per-token bill
- A local artifact you can inspect, serve, or fine-tune
- SmolLM2 135M parameters, ~261 MB on this laptop
- Downloads once, then works with no network
- It is now a local artifact you control
- Size is two different numbers: **parameters** drive quality, **bytes on disk** drive whether you can ship it. M2 comes back to this.

<!--
Try this: open the local model folder or its Hugging Face files page. A model is
not one opaque object; it is weights, a tokenizer, configuration, and metadata.

The two-numbers point matters and people conflate them: 135M parameters is the
capability number; roughly 261 MB is the logistics number here. A model can be small on disk
and still useless, or large on disk and cheap to run. M2's IQ/size/cost table is
where this gets resolved.

This particular model is SmolLM2 135M Instruct. It is a small local text model
for demonstrating the ownership boundary; later modules use their own models
for embeddings and RAG.

The first model run may take longer because weights must be loaded into memory.
Later runs reuse the local files, but still need enough memory to load the model.
-->

---

# M0.2.4 · Call A Hosted Model

```python
import os

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-2.5-flash-lite", contents="Say hello."
)
print(response.text)
```

Full running version: `CODEALONGS/day_1/m0_section_2_model_access/03_gemini_api.py`

- Same prompt → response shape
- Model runs at Google's boundary, not on this laptop
- The API key authorizes a billed request

<!--
Compare this directly with the local-model snippet. Both use a short
prompt-to-response flow; what changes is where the model runs, where the data
travels, who operates the infrastructure, and how usage is billed.
-->

---

<!-- _class: lead -->

# M0.3.1 · Build One Small Application

We will grow one synthetic wealth demo: value → functions → classes → SQLite → server → logs, tests, and debugging.

<!--
**Instructor only:** This is the transition into the hands-on portion. Have
participants open the Section 3 folder before advancing.

Framing: we're not covering "all of Python". We're growing one small wealth
application through the Python engineering moves used throughout the week.
Every material is in `CODEALONGS/day_1/m0_section_3_wealth_demo/`; snippets run
with `uv run --project CODEALONGS python <snippet-path>`.
-->

---

**Wealth Demo · 1–2 of 9**

# M0.3.2 · Variables & Type Hints

```python
symbol: str = "AAPL"
shares: int = 10
purchase_price: float = 80.50

purchase_cost: float = shares * purchase_price
print(f"{symbol} purchase cost: {purchase_cost}")
```

Snippet: `CODEALONGS/day_1/m0_section_3_wealth_demo/01_variables_and_hints.py`

**What to notice**

- No type declarations needed to run
- Use annotations to state what crosses an interface
- Let Python infer obvious short-lived local values
- A type hint documents intent; it does not validate a value at runtime

<!--
Python can infer the type of many local values. Type hints are most valuable on
function signatures and data models, where another reader needs to understand
the expected inputs and outputs before reading the implementation.

Type hints make the public shape of a function or data model readable before
participants see its implementation.
-->

---

**Wealth Demo · 3 of 9**

# M0.3.3 · Functions

```python
def purchase_cost(shares: int, price: float) -> float:
    """Return the cost of buying shares at a price."""
    if shares <= 0 or price <= 0:
        raise ValueError("Shares and price must be positive.")
    return shares * price
```

Snippet and code-along: `CODEALONGS/day_1/m0_section_3_wealth_demo/03_functions.py` → `04_functions_code_along.ipynb`

**What to notice**

- One job, descriptive name, docstring, type hints, and return value
- Reject bad financial inputs clearly
- We add logging after there is an application worth operating

<!--
Keep a function focused on one reusable job. Logging belongs at the application
boundary later in the module, where there are requests, database operations, and
failures worth tracing.
-->

---

**Wealth Demo · 4 of 9**

# M0.3.4 · Classes

```python
from dataclasses import dataclass


@dataclass
class Holding:
    symbol: str
    shares: int
    purchase_price: float

    def market_value(self, latest_price: float) -> float:
        """Return this holding's current market value."""
        return self.shares * latest_price
```

Snippet and code-along: `CODEALONGS/day_1/m0_section_3_wealth_demo/05_classes.py` → `06_classes_code_along.ipynb`

**What to notice**

- A dataclass gives structured data a name
- A method is behavior that belongs with that data
- The code-along adds `Portfolio.buy()` and its insufficient-cash rule

<!--
One advanced dataclass rule: a mutable default such as `items=[]` would be
shared across instances. Use `field(default_factory=list)` when a dataclass
needs a fresh list for every object.

Most AI application code favors composition—small objects working together—over
deep inheritance hierarchies. `Holding` and `Portfolio` are separate objects
with clear responsibilities.
-->

---

**Wealth Demo · 5 of 9**

# M0.3.5 · Store Data in SQLite

```python
import sqlite3

connection = sqlite3.connect(":memory:")
connection.execute("CREATE TABLE prices (symbol TEXT, date TEXT, close REAL)")
connection.execute("INSERT INTO prices VALUES (?, ?, ?)", ("AAPL", "2020-06-01", 80.46))

row = connection.execute(
    "SELECT close FROM prices WHERE symbol = ? AND date <= ? "
    "ORDER BY date DESC LIMIT 1",
    ("AAPL", "2020-06-01"),
).fetchone()
```

Snippet and code-along: `CODEALONGS/day_1/m0_section_3_wealth_demo/07_database.py` → `08_database_code_along.ipynb`

**What to notice**

- `sqlite3` is included with Python
- `?` placeholders are compulsory; never f-string values into SQL
- `date <= ?` prevents using information unavailable at that historical date

<!--
SQL placeholders keep values separate from SQL instructions. Building a query
with an f-string can turn untrusted input into executable SQL; this risk is even
greater when a value originated from a user or a model.

The historical-date rule is equally important: a backtest must not use a price
that was unknown on the requested date. The lab later makes this an intentional
debugging exercise.
-->

---

**Wealth Demo · 6 of 9**

# M0.3.6 · Run a Local Server

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    """Confirm that the application is running."""
    return {"status": "ok"}
```

Snippet and code-along: `CODEALONGS/day_1/m0_section_3_wealth_demo/09_server.py` → `10_server_code_along.ipynb`

**What to notice**

- `@app.get("/health")` connects a URL to a Python function
- `GET /portfolio` loads synthetic data and FastAPI returns JSON
- Install: `uv add fastapi uvicorn`
- Run the complete `wealth_demo.server:app` from the next slide's command block
- Explore it interactively at `http://127.0.0.1:8000/docs`

<!--
FastAPI lets participants see the application boundary without teaching HTTP
handler internals. The route decorator is the essential idea; `/docs` makes the
API contract visible immediately. Later modules add AI-backed routes to this
same application shape.
-->

---

**Wealth Demo · 7–9 of 9**

# M0.3.7 · Logging, Testing & Debugging

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

symbol = "AAPL"
selected_date = "2020-06-01"
logger.info("Selected %s price dated %s", symbol, selected_date)
```

Snippet and code-along: `CODEALONGS/day_1/m0_section_3_wealth_demo/11_logging_testing_debugging.py` → `12_logging_testing_debugging_code_along.ipynb`

**What to notice**

- `INFO`: normal startup, request, and database activity
- `WARNING`: expected invalid input or unknown route
- `exception()`: unexpected failure with a traceback

**Run and test the complete application**

```bash
cd CODEALONGS/day_1/m0_section_3_wealth_demo
uv run uvicorn wealth_demo.server:app --reload
uv run python -m unittest wealth_demo.test_wealth_demo -v
```
- Debug the intentional date-query bug from its failing test and selected-date log
- Escalate to `uv run pytest -x --pdb` or `breakpoint()` only when needed

<!--
Run the local server from `CODEALONGS/day_1/m0_section_3_wealth_demo`, then
visit `/health` and `/portfolio`. The debugging exercise changes the date query
to the wrong direction; use the failed test and the INFO log's selected date to
identify and correct it.
-->

---

# M0.L1 · Lab: Build the Wealth Demo

**Mini lab — 20 minutes**

Use synthetic AAPL data to complete `purchase_cost`, `gain_loss`, and one
SQLite point-in-time lookup. Run the supplied tests until they pass.

**Main lab — 1–2 hours**

Complete a small wealth service that can:

1. buy a validated holding from a cash balance
2. store and retrieve holdings in SQLite
3. serve `GET /portfolio` using FastAPI
4. log a request and fix an intentionally incorrect date query

Done when: the calculation, portfolio, database, and API tests pass; `/docs`
can call the working `/portfolio` route.

The participant brief, hints, inspiration solution, and instructor solution are
the next courseware pack to add for this lab.

<!--
The mini lab isolates the essentials. The main lab combines the same components
in the order participants just learned them. Keep the data synthetic: the goal
is Python engineering, not market-data wrangling. The date query is the
debugging exercise: the selected price must be on or before the requested date.
-->

---

# M0.4.1 · Python → IPython → Jupyter

**The Java/C loop**

Write it all → compile → test → *hope*

You commit to the design before you see it run.

```bash
uv run --project CODEALONGS python       # run a snippet or bare REPL
uv run --project CODEALONGS ipython      # + history, %timeit
uv run --project CODEALONGS jupyter lab  # open guided code-alongs
```

**The Python loop**

Write a line → **look at it** → change it

Python is glue code. You write it *on the way* to making it work — run it, read the output, learn something, adjust.

That's not sloppiness. It's the same loop a data analyst uses, and it's why the language ended up owning analytics **and** AI.

> Notebooks are for *exploring*. Modules are for *shipping*.
> Prototype in Jupyter, then move the code into `.py` files.

In this course: use a small `.py` snippet to learn one idea, a notebook to
explore it, then `wealth_demo/` modules to ship it.

<!--
The commands support a working style: use the fastest feedback loop that fits
the question you are answering.

The contrast to draw: in Java or C the loop is expensive — compile, wait, run —
so you think hard up front and commit to a design before you see it execute.
Python's loop is nearly free, so you find the design by running things. Neither
is better in the abstract; they suit different problems.

For AI work the fast loop is decisive, because you genuinely cannot predict what
a model will do with your data. You have to look. That is why every AI tutorial
you will ever see is a notebook.

IPython adds useful exploration ergonomics: tab completion, `?` for a docstring,
and `%timeit` for measuring a small operation. It is the same Python runtime
with a better interactive loop.

Notebooks can contain imports and tests, but their execution order and state can
be hidden. Use them to explore data and behavior; move stable, reusable logic
into modules that can be imported, tested, and reviewed in version control.
-->

---

<!-- _class: lead -->

# M0.5.1 · Maintainable Python & the Zen

**Make code easy for a teammate — or an AI — to read and change.**

```python
# Before
def v(s, p): return s * p

# After
def market_value(shares: int, price: float) -> float:
    """Return the current value of a holding."""
    return shares * price
```

- Use descriptive names: `portfolio_value`, not `pv`
- One job per function and one responsibility per file
- Keep docstrings, type hints, logs, and tests close to the behavior they explain
- Explore in notebooks; ship readable `.py` modules

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
