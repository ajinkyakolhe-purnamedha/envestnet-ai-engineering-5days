> **⚠️ OUTDATED** — These lab instructions are out of date (paths and setup
> may no longer match the repo). Reworked labs are coming later.

# M9 Lab — Everything You Built, Gated

You finish the advisor assistant: your M8 workflow's drafts go behind a
**human approval gate**, the assistant gains **memory**, and (stretch) a
**model judge** gives a second opinion. The UI is given and already
wired — you write four functions and watch two dashboards come alive.

**60 minutes. The payoff lands at the halfway mark** — build in the
order below, which is NOT deck order: gate first.

No warm-up section this time: you already ran the `m9/` toys during the
module's three experiments.

---

## The map

Work in `CAPSTONE-PROJECT/chronos_wealth_management/labs/m9_advisor_assistant/`.

```text
submit_note_for_approval.py   YOU · 1   the gate's intake
decide_note_draft.py          YOU · 2   the human decision
answer_with_memory.py         YOU · 3   the memory seam
judge_note_with_model.py      YOU · S   stretch: rung 2
m8_reference_assistant.py     given     M8 stand-in for M9
condense_conversation_history given     windowing helper
note_draft_queries.py         given     reads + row builder
model_loading.py              given     re-exported from M8
```

Your progress meter — 13 tests in build order (+2 stretch skips):

```bash
cd CAPSTONE-PROJECT/chronos_wealth_management
uv run python -m pytest labs/m9_advisor_assistant -q
```

These tests grade **your M9 code only**. M9 includes a compact reference
version of yesterday's assistant, so an unfinished M8 lab does not block
the tests or the live UI. If your M8 solution is complete, swapping it
back in is a stretch after M9 is green.

Before step 1, spend ten minutes reading the given code — all of it is
short: `note_draft_queries.py` (the client-visibility rule lives here,
plus `build_note_draft_response` and the three status constants your
stubs will import) and the four routes in
`api_routes/advisor_workspace_routes.py` (house pattern: role checks,
`translate_domain_errors()`, function-level lab imports, 501 while a
stub is missing).

---

## Step 1 · `submit_note_for_approval.py` — the intake (~10 min)

Every portfolio answer becomes a **pending row** in
`advisor_note_drafts`. Copy the answer's fields onto an
`AdvisorNoteDraft` row (`review_problems` as JSON), status
`PENDING_STATUS` — always; only step 2 may ever set anything else.
`created_simulated_date` comes from the client's account — the app's
clock, never the wall clock. `db.add` + `db.flush()`; the session owner
commits.

Tests 1–3 go green. On the dashboard, the assistant's answers now show
"Draft #N sent to the approval queue" and the queue panel fills.

## Step 2 · `decide_note_draft.py` — the decision (~10 min)

Approve or reject, with a reason. Unknown id →
`RecordNotFoundError`. A draft that is not pending →
`NoteDraftAlreadyDecidedError` — decisions are final, there is no
un-approve. This function is the **only code in the app allowed to set
an approved status**.

Tests 4–9 go green (4–6 direct, 7–9 over HTTP). **This is the payoff:**

1. Advisor dashboard → Assistant panel → ask a portfolio question.
2. Approval Queue → read the note, the rule problems, the judge column
   (— until the stretch) → **Approve**.
3. Log out, log in as `alice@example.com` → **"Messages From Your
   Advisor"** — your note, on the client's screen.
4. Ask again, **Reject** this one → Alice never sees it. Ever.

Then the durability demo: kill uvicorn mid-queue, restart — the pending
draft is still there. A row survives; a variable would not.

## Step 3 · `answer_with_memory.py` — the memory seam (~20 min)

Fix M9.1.2's amnesia: window the history with the given
`condense_conversation_history` (keep the module-level import — the
tests patch it by name), join the windowed turns and the new question
into one **effective question** (new question LAST), and hand it to
`answer_client_question_for_m9` with the windowed history.

Safety comes free: a trade word in the new turn makes the effective
question route to `"trade"`, so refusals still fire mid-conversation.

Tests 10–12 go green. In your chat panel, the module's opening failure
is now fixed by your own code:

```text
"What does the concentration guideline say?"  -> policy
"Why is that a problem for Alice?"            -> policy (thread kept)
```

## Stretch · `judge_note_with_model.py` — rung 2

One more model call, one closed question, defensive parsing (only a
reply leading with "yes" counts — hedges and essays fail to NO). `None`
when no model is installed: the rung is skipped, never faked. Its two
tests un-skip, and the queue's judge column comes alive. Remember the
measured 2/6 — the judge **advises**; it never blocks.

---

## Acceptance

```bash
cd CAPSTONE-PROJECT/chronos_wealth_management
# your build: 13 green + 2 stretch skips
uv run python -m pytest labs/m9_advisor_assistant -q
# the shipped suite stays green throughout
uv run python -m pytest -q
```

- Ask → pending draft in the queue → Approve → note on Alice's
  dashboard; Reject → Alice never sees it
- Kill and restart the API: the pending queue survives
- The M9.1.2 follow-up now stays on thread in your chat panel
- Submitting can never create an approved row; re-deciding a decided
  draft is a 409

> **Gotcha (same as yesterday):** always run tests as
> `uv run python -m pytest`. A bare `uv run pytest` can silently pick
> up a PATH pytest (e.g. conda's) with the wrong Python when the venv
> and extras are out of sync.

---

## Stretch options, in payoff order

1. **The judge** — see above; completes the ladder in the product.
2. **Judge, better** — reword the prompt in `m9/llm_judge.py`
   (SLIDES-markdown), re-run, beat the measured 2/6 agreement. That
   loop — reword, re-measure — is judge engineering.
3. **Stream it** — SSE endpoint behind the draft function (the single
   swap point), `st.write_stream` in the chat panel.
4. **Summarize the memory** — swap the deterministic fold for a
   SmolLM2 summary; watch which tests break and why (determinism, and
   the router keywords the summary drops).
5. **Read Day 4** — list every hardwired tool in the assistant
   (`gather_client_facts`, the thresholds, the price lookups). Which
   would MCP externalize tomorrow?
6. **Swap in your M8** — replace the M9 reference assistant with your
   completed M8 workflow and verify the same gate still works.
