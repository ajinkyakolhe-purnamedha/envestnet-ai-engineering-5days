> **⚠️ OUTDATED** — These lab instructions are out of date (paths and setup
> may no longer match the repo). Reworked labs are coming later.

# M8 Lab — Ship The Advisor Assistant Into Chronos

You will build a real agentic feature inside the capstone: ask the Chronos
API an advisor question, get back a routed, fact-grounded, rule-checked
advisor note. The morning's patterns — routing, chaining, evaluator — become
production code with business-readable names.

**The lab rule:** the code-alongs are examples (hardcoded prices, dict tools).
Nothing pastes into the capstone — real schemas, a real DB session, the
point-in-time price rule. You design from the patterns; you write from the
interfaces.

---

## Part A · Warm-up (10 minutes, offline)

From the repo root (the snippets live in `SLIDES-markdown/m8/`; the
`uv` environment lives in `CODE-ALONGS/`):

```bash
cd SLIDES-markdown
uv sync --project ../CODE-ALONGS --extra agents
# the trace from the framework run
uv run --project ../CODE-ALONGS python m8/smolagents_agent.py
# the fix
uv run --project ../CODE-ALONGS python m8/pattern_chaining.py
# the front door
uv run --project ../CODE-ALONGS python m8/pattern_routing.py
```

Read each trace. You are about to rebuild this workflow over real data.

---

## Part B · Implement the starter pack

Work in `CAPSTONE-PROJECT/chronos_wealth_management/labs/m8_advisor_assistant/`.
The five functions you learned this morning are **stubs that raise
`NotImplementedError`** — you write them. The plumbing you did not learn
today (`gather_client_facts.py`, `model_loading.py`) is given complete.

Your progress meter — run it constantly, watch 15 tests go green file by
file (the last two call your workflow over HTTP):

```bash
cd CAPSTONE-PROJECT/chronos_wealth_management
uv run python -m pytest labs/m8_advisor_assistant -q
```

Build in this order; each step names what already exists for you to reuse.

### 1. `route_client_question.py` — the front door

`route_client_question(question: str) -> str` returning `"portfolio"`,
`"policy"`, or `"trade"`. A keyword router is enough — and it must
recognize sell-shaped phrasings (`sell`, `liquidate`, `cash out`,
`dump`...). Trade questions will be *refused before any tool runs*.

### 2. `gather_client_facts.py` — the facts (GIVEN — read it)

Provided complete: `gather_client_facts(db, client_user_id)` returns the
portfolio snapshot, metrics, and recommendations by composing:

- `get_account_for_investor_user` (investor_accounts)
- `build_current_portfolio_snapshot` (portfolio_performance)
- `analyze_client_portfolio`, `build_advisor_recommendations`
  (advisor_workspace)

Gather **sequentially**. The M8.2.4 fan-out does not apply here: these
lookups share one SQLAlchemy session, and sessions are not thread-safe.
Parallelize independent services, not a shared connection.

### 3. `judge_against_guidelines.py` — the verdict

`judge_against_guidelines(metrics) -> str`. Reuse
`CONCENTRATION_THRESHOLD` and `HIGH_CASH_THRESHOLD` from
`advisor_workspace.analyze_client_portfolio` — do not restate `0.35`.
Python owns this decision; the model never sees it undecided.

### 4. `draft_advisor_note.py` — prose only

`draft_advisor_note(question, metrics, verdict, recommendations)
-> (note, note_source)`.

- `model_loading.py` is given: `load_offline_language_model()` returns a
  cached transformers pipeline over the committed SmolLM2 weights, or
  `None` when the `agents` extra is missing or anything fails to load.
- `None` means: return a deterministic template note built from the
  metrics and verdict, with `note_source == "template"` — a broken or
  absent install must never break the API.
- With a pipeline: draft the note (the stub's docstring shows the exact
  call shape).

The prompt must state the verdict as already decided. The model writes
sentences; it decides nothing.

### 5. `review_advisor_note.py` — the gate

`review_advisor_note(note, verdict) -> list[str]` of problems:
a blocked verdict must be cited (the note mentions the breached
threshold figure), and the note stays under 80 words.

### 6. `answer_client_question.py` — the workflow

Route, then:

- `"trade"` → refuse: no gather, `refused=True`, explain why.
- `"policy"` → answer from the thresholds, no client data.
- `"portfolio"` → gather → judge → draft → review; if the review finds
  problems, redraft **once** (a bound, like `max_turns`), re-review, and
  return any remaining problems with the response.

Accept `conversation_history: list[str] | None = None` and ignore it —
that parameter is where M9 will attach memory.

### 7. Ship it — your code IS the feature

The API endpoint `POST /advisor/clients/{client_user_id}/assistant`
serves **your** `labs/m8_advisor_assistant` package. Until your stubs
are implemented it answers `501 — complete the M8 lab`; when your tests
go green, the feature is live. The last two lab tests call it over HTTP.

Read how the house pattern wires it in
`api_routes/advisor_workspace_routes.py` (`advisor_user_id` param, role
checks, `translate_domain_errors()`), then hit it against the running
app and watch your own workflow answer.

---

## Acceptance

```bash
cd CAPSTONE-PROJECT/chronos_wealth_management
# your build: 15 green (13 workflow + 2 over HTTP)
uv run python -m pytest labs/m8_advisor_assistant -q
# the shipped suite stays green throughout
uv run python -m pytest -q
```

- Trade-shaped questions → `refused=True`, metrics `None`, no data read
- Portfolio question → verdict matches `analyze_client_portfolio`, note
  cites the breached threshold, `review_problems == []`
- With no model installed → `note_source == "template"` and everything
  above still holds
- Investor calling the endpoint as advisor → `403`
- Full suite still green: `uv run python -m pytest -q`

Then install the model and watch the same feature upgrade itself:

```bash
uv sync --extra agents
uv run --extra agents python -m pytest \
    labs/m8_advisor_assistant -q
```

`note_source` flips to `"language_model"` with zero code change — the
draft function is the swap point.

Two things to expect during the live run:

- **A fresh Alice is 100% cash**, so the verdict you'll see first is the
  *40% cash* breach. To watch the 35% concentration verdict fire, log in
  as Alice and buy AAPL until it dominates the portfolio, then ask again.
  Two different breaches exercise the same workflow, and Python catches both.
- **SmolLM2's prose will be mediocre** (it is a 135M model — you watched
  it fail this morning). Read the note critically: the *sentences* may be weak,
  but the verdict and every figure stay correct, because Python computed
  them and the model only phrased them. That separation is what the chaining
  pattern gives you.

> **Gotcha:** always run tests as `uv run python -m pytest`. If the venv
> and extras are out of sync, bare `uv run pytest` can silently pick up a
> pytest from your PATH (e.g. conda) with the wrong Python entirely.

---

## Stretch

1. **Router showdown** — upgrade the keyword router to BGE embeddings
   (the M2 pattern), then test `"How much cash would selling AAPL raise?"`
   against both. The embedding router misroutes it to price; your keyword
   router refuses it. Write one sentence: why is the keyword router safer
   here, and what would make the embedding router safe?
2. **Trace habit** — add `elapsed_ms` per workflow step to the response.
3. **Close the loop** — point the CODE-ALONGS smolagents example's tools at
   the running Chronos API instead of its hardcoded dicts.
4. **Read tomorrow** — list what M9 must add to make this client-facing:
   memory, a human approval gate, streaming. Find the extension point for each in
   today's code.
