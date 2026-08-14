---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M9.0.1 · Memory, Verification & The Human Gate

Yesterday you composed the workflow. Today you finish it.

By the end of this module you can:

- Give an assistant memory — and bound what it remembers
- Check its work three ways: rules, a model judge, a human
- Put an approval gate between a draft and a client
- Ship all of it into the Chronos advisor dashboard

<!--
Three verbs organize the whole day: remember, verify, gate. The M8 lab
ended with a working advisor assistant that routes, refuses trades,
grounds its facts in Python, and checks its own draft with rules. What it
still cannot do: hold a conversation, get a second opinion, or put a
human between its draft and a client. Day 3 lands here — M7 built the
loop, M8 composed the workflow, M9 turns that workflow into a finished
feature a real advisory firm could defend.

One idea runs through the middle of the module and is worth naming early:
rule checks, LLM-as-judge, and human approval are not three separate
topics. They are three implementations of ONE job — verifying the
agent's work — that differ in cost, latency, and what they catch. The
module treats them as a ladder and climbs it.
-->

---

<!-- _class: lead -->

# M9.1.1 · What You Shipped Yesterday

The M8 assistant, honestly scored:

```text
routes questions        yes — keyword front door
refuses trades          yes — before any tool runs
grounds every figure    yes — Python computed them
checks its own draft    yes — rules, one revision

remembers the last turn         NO
gets a second opinion           NO — rules only
asks a human before shipping    NO
```

<!--
The scorecard's top half is real engineering: the M8 lab produced a
feature that answers advisor questions with facts Python computed and a
verdict Python decided, checked by a rule-based reviewer with one bounded
revision. Everything an LLM could get wrong was taken away from it.

The bottom half is what separates a demo from a product. Every request is
an orphan — ask a follow-up and the assistant has never heard of the
conversation. Verification is rules-only — an unpredicted failure mode
sails through. And nothing stands between the drafted note and whoever
reads it. All three gaps close today, and each closure lands in the same
capstone package the M8 lab built, not in a new toy.
-->

---

# M9.1.2 · Watch It Forget

Two questions to yesterday's endpoint, in order:

```text
Q1  "What does the concentration guideline say?"
    route: policy -> the 35% / 40% thresholds

Q2  "Why is that a problem for Alice?"
    route: portfolio -> generic portfolio note
```

Q2 continued the policy thread. The assistant never knew.

<!--
The failure is mechanical and worth tracing precisely. The router sees
only the bare question. Q1 contains "guideline" — a policy word — and
routes correctly. Q2 contains no route keyword at all, so it falls
through to the default portfolio route: the workflow gathers facts,
judges, and drafts a competent note about the portfolio in general —
a fluent answer to a question nobody asked. The thread that gave Q2 its
meaning ("that" = the concentration limit) lived only in the advisor's
head.

Statelessness was a deliberate M8 simplification, marked at the time: the
workflow accepts a conversation_history parameter and ignores it — the
seam left for today. The fix is not an architecture change; it is using
one list that already exists in the signature.
-->

---

# M9.1.3 · Experiment: Break It Yourself

With your API and UI running, on the advisor dashboard:

```text
1. Assistant panel: ask the two questions from the
   last slide, in order.
2. First answer arrives. The follow-up does not:
   501 — "complete the lab: M9 lab step 3"
```

```text
Checkpoint: the assistant answers orphans only.
The chat panel already sends the history;
nothing on the server accepts it yet.
The fix is one list.
```

<!--
The advisor dashboard gained an Assistant chat panel overnight, and it is
honest about today's state: it remembers the conversation client-side and
sends it with every request, but the server-side seam that would use it
is a stub. The first question works (empty history takes yesterday's M8
path). The moment a second turn carries history, the endpoint answers
501 and names the missing piece — answer_with_memory, lab step 3.

Anyone who wants the semantic version of the failure instead of the
structural one can ask Q2 as a fresh first question: it routes to
portfolio and drafts an off-thread note, exactly as the previous slide
traced. Both failures are the same fact seen twice: the transcript
exists, and nothing reads it. That is the whole gap between yesterday's
assistant and a conversation.
-->

---

**Memory · 1 of 6**

# M9.2.1 · Memory Is Just The Transcript

No new machinery. Past turns travel with the request:

```text
st.session_state          the panel keeps the turns
        |
POST /assistant           "conversation_history": [...]
        |
answer_with_memory        the seam, finally used
```

In-context memory: the model re-reads, every turn.

<!--
The word "memory" suggests something stored inside the model. Nothing is.
A language model call is a pure function of its prompt — so conversation
memory means one thing: the transcript rides along and gets re-read on
every turn. Chat products all work this way at the core; the
sophistication is in what makes it into the transcript, not in the
mechanism.

The Chronos wiring makes each hop visible. The Streamlit panel holds the
turn list in st.session_state (client-side, per advisor+client pair). It
sends the list as conversation_history in the request body — the field
added to the ask schema today. The endpoint hands it to
answer_with_memory, the function that finally uses the parameter M8
accepted and ignored. One design choice matters ahead of its slide: the
history stores the advisor's past QUESTIONS, not the assistant's answers
— the reason arrives with the routing slide.
-->

---

**Memory · 2 of 6**

# M9.2.2 · The Transcript Grows

Six turns of one advisor chat, measured:

```text
turn 1     29 tokens
turn 2     51
turn 3     74
turn 4     97
turn 5    118
turn 6    135        every one re-sent, every turn
```

Linear growth, forever. The context window is not forever.

<!--
Numbers from m9/memory_window.py running the SmolLM2 tokenizer over a
six-turn advisor conversation (question plus answer each turn): 29 tokens
after turn one, 135 after turn six, about 20-25 added per turn. Toy
sizes, real shape — the growth is linear and unbounded, and every token
is re-sent and re-processed on every subsequent turn, so cost grows
quadratically over a conversation's life even while each turn's growth
is linear.

M2 set the budget this collides with: every model has a finite context
window, and long before the hard limit, retrieval quality and attention
degrade as prompts bloat. A production chat feature therefore never
ships "append forever" — something must bound the transcript. The next
slides are the three standard bounds.
-->

---

**Memory · 3 of 6**

# M9.2.3 · Experiment: Watch It Grow

From `SLIDES-markdown/`:

```bash
uv run --project ../CODE-ALONGS \
    python m9/memory_window.py
uv run --project ../CODE-ALONGS \
    python m9/memory_summarize.py
```

For the second run: **which numbers survived?**

```text
Checkpoint: the transcript is the memory, it
grows linearly, and folding it has a price —
exact words survive, or style survives. Pick.
```

<!--
Two runs, two lessons. memory_window prints the growth table from the
last slide live, then windows the history — last four entries verbatim,
older turns folded into one truncated line — and the count drops from
135 to 89 tokens. The saving looks modest at six turns; the point is the
asymptote. The full transcript grows without bound, the window does not.

memory_summarize hands the same old turns to SmolLM2 and asks for a
one-sentence summary, keeping every number. The measured result: the
conversation held three figures ($104,120 value, 4.1% return, 52% vs
35% concentration) and the model's summary kept only the last one —
it echoed the most recent turn and silently dropped the rest. 56 tokens
became 20, and two facts died. That is the general trade of model-written
summaries: fluent, compact, lossy — and the loss is silent. The
deterministic fold is ugly but keeps exactly what it was told to keep.
-->

---

**Memory · 4 of 6**

# M9.2.4 · Keep, Fold, Or Store

Three ways to bound a transcript:

```text
window      keep last N turns verbatim
            exact, cheap; older context gone

summarize   fold old turns via the model
            compact, fluent; loss is SILENT
            (measured: 3 figures in, 1 out)

store       put turns in a database, retrieve
            unbounded past; that is M4's RAG
```

<!--
The three strategies stack in practice: production chat systems commonly
window the recent turns, summarize the middle distance, and push the
deep past into a retrieval store. Each rung trades exactness for reach.

The window is the honest default and what the capstone uses — the given
condense_conversation_history helper keeps the last four turns verbatim
and folds older ones into a single deterministic line. Summarization
buys fluency at the cost the experiment just measured: the model decides
what matters, and it decided wrong two times out of three. The external
store closes a loop from Day 2 — "memory beyond the window" is exactly
the retrieval problem M4 solved, with the transcript as the corpus.
Recognizing that RAG and long-term chat memory are the same machinery is
one of those unifications that makes both easier to reason about.
-->

---

**Memory · 5 of 6**

# M9.2.5 · The Effective Question

Route on the conversation, not the orphan:

```text
history  ["What does the concentration
           guideline say?"]
turn     "Why is that a problem for Alice?"

effective = windowed history + new turn
route(effective)  ->  policy   (thread kept)
```

New question goes LAST. Most recent wins.

<!--
This is the whole fix for M9.1.2, and it is lab step 3. The follow-up is
not answered as itself; it is answered as the tail of an effective
question — the windowed history joined with the new turn. The router now
sees "guideline" from the opener and keeps the policy thread. The
drafter sees the same context. No component changed; only the input got
smarter.

Two properties come free and both are load-bearing. Trade safety: a
trade word in the NEW turn makes the effective question route to trade,
so refusals still fire mid-conversation. And the questions-only rule
from M9.2.1 earns its keep here: assistant answers contain words like
"guidelines" (every verdict does), so storing answers would drag every
later turn toward the policy route — the note's own vocabulary would
hijack the router. Remembering questions only keeps the routing signal
clean. The refused turns are excluded for the same reason: their trade
words would poison every turn after them.
-->

---

**Memory · 6 of 6**

# M9.2.6 · What Never Goes In Memory

Memory is scoped per **(advisor, client)** pair.

```text
in the transcript:
  the advisor's past questions for THIS client

never in the transcript:
  other clients' holdings or names
  refused (trade-shaped) turns
  anything the role could not see fresh
```

Memory must not out-privilege the question it serves.

<!--
Memory is an accumulation of data, and accumulated data inherits every
access-control question the original data had. The rule that keeps it
safe: a transcript may never let a request see what the same request
could not fetch fresh. Scoping the panel's history per advisor-client
pair enforces that structurally — Bob's numbers cannot leak into a
conversation about Alice because they were never in Alice's transcript.

The other two exclusions repeat earlier reasoning at the policy level:
refused turns stay out so trade vocabulary cannot poison the router, and
in a real deployment the transcript is also where PII quietly pools —
which makes "what goes in memory" a compliance question, not just an
engineering one. In finance, a chat transcript that includes client
positions is a record subject to retention rules. Design the memory
scope on day one; retrofitting it after a leak is the expensive order.
-->

---

<!-- _class: lead -->

**The Verification Ladder · 1 of 7**

# M9.3.1 · One Job, Three Verifiers

"Is this note good enough to send?" — three answers:

```text
rung  verifier        cost        catches
 1    Python rules    ~free       what you predicted
 2    model judge     +1 call     fuzzy quality — maybe
 3    a human         minutes     what nobody imagined
```

Not alternatives. They **stack**.

<!--
The organizing insight of the module: rule checks, LLM-as-judge, and
human approval look like three different topics — a code review
practice, a prompting technique, a UX pattern. They are one job,
implemented three ways. Each rung costs more and catches more: rules are
free and instant but only ever catch failure modes someone predicted;
a model judge costs one more call and can evaluate fuzzy qualities no
regex can express — if the judge is competent, which gets measured
shortly; a human costs real minutes and a queue, and catches the failure
mode nobody imagined, which is the only rung that can.

Because they stack rather than compete, the design question is never
"which one?" but "how many rungs does THIS output need?" — the module
closes the section with that choice. The M8 lab already built rung 1;
this section adds the other two on top of the same artifact.
-->

---

**The Verification Ladder · 2 of 7**

# M9.3.2 · Rung 1: You Already Built It

`review_advisor_note` — yesterday, lab step 5:

```text
blocked verdict must cite the threshold figure
note stays under 80 words
     -> problems found -> ONE redraft -> re-check
```

Free, instant, deterministic. And blind:

it will never catch a note that is fluent, cited, **wrong**.

<!--
Yesterday's evaluator gate, reread through the ladder. Its two rules
encode predicted failure modes: a note that hides the breached
threshold, and a note that rambles. Within that prediction it is
perfect — exact, free, instant, testable, the same verdict every run.
Rules like these should guard every LLM output everywhere; there is no
cost argument against them.

Their blindness is structural, not fixable with more rules: every rule
encodes a failure someone already imagined. A note that states the right
threshold figure while drawing a subtly wrong conclusion from it passes
both checks with a perfect score. The rule count can grow forever and
the un-imagined failure stays one step ahead. That gap — plausible,
compliant, wrong — is what the next two rungs exist for.
-->

---

**The Verification Ladder · 3 of 7**

# M9.3.3 · Rung 2: A Model As Judge

One more call, one closed question:

```python
def model_judge(note: str) -> bool:
    reply = generate(
        f'Note: "{note}"\nDoes the note cite a '
        "specific threshold percentage? "
        "Answer YES or NO.",
        max_new_tokens=8)
    return reply.strip().lower().startswith("yes")
```

Parse defensively. Small models ramble.

<!--
The recipe is deliberately minimal: give the judge the artifact, ask ONE
yes/no question, cap the output, and parse defensively — only a reply
that leads with "yes" counts, so hedges, apologies, and essays all fail
closed to NO. Closed questions are the difference between a judge and a
book report; a judge asked "is this note good?" produces vibes, a judge
asked "does it cite a threshold percentage?" produces a checkable claim.

This is a single judge inside one workflow — the smallest unit of a much
bigger discipline. Scoring whole systems with judge models, calibrating
judges against human labels, and building eval suites is Day 5's
territory. Today's question is narrower and prior to all of that: can
the model at hand judge at all? The next slide measures it instead of
assuming either way.
-->

---

**The Verification Ladder · 4 of 7**

# M9.3.4 · Experiment: Can 135M Judge?

```bash
uv run --project ../CODE-ALONGS \
    python m9/llm_judge.py
```

Six notes — three cite a threshold, three don't:

```text
measured: judge agrees with the rule  2/6
          judge said YES              5/6
```

The judge is a **yes-man**.

```text
Checkpoint: rung 2 is real, but it is only as
strong as the judge model. Ours approves
everything. It may advise; it must not block.
```

<!--
The measured result, greedy decoding, reproducible: on six notes where
the ground truth is trivially checkable by the rule, SmolLM2-135M agreed
with the rule twice. The failure has a shape, not just a rate — the
judge said YES to five of six notes, including all three that cite no
figure at all, and its only NO landed on a note that does. It is not a
weak judge; it is a sycophant, and sycophancy is the characteristic
failure of small judge models: agreement is the statistically safest
continuation.

The design consequence is exactly how the capstone wires this rung: the
judge's verdict is displayed in the approval queue next to the rule
check, and it never blocks anything. An unreliable verifier that can
veto work is worse than no verifier — it adds noise with authority. An
unreliable verifier that only advises costs one call and occasionally
catches something. Frontier models judge far better than 135M — but
"how much better, measured?" is the Day 5 question, and the burden of
proof always sits with the judge before it gets a veto.
-->

---

**The Verification Ladder · 5 of 7**

# M9.3.5 · A Judge Is Only As Good As The Judge

What the 2/6 teaches, beyond SmolLM2:

```text
judge quality  =  model quality on THAT question
prompt shape moves the verdict
agreement must be MEASURED, never assumed

deploy rule: a judge starts advisory.
it earns a veto with data, or it never gets one.
```

<!--
The generalization, stated carefully because it cuts both ways. Nothing
here says LLM-as-judge is fake — at frontier scale it is a standard,
effective technique and much of modern evaluation runs on it. It says
that a judge is a model output like any other: sensitive to prompt
wording, prone to systematic bias (sycophancy, position bias,
verbosity preference are all documented), and unverified until someone
measures its agreement against ground truth on the actual task. The 2/6
was measurable in thirty seconds precisely because the toy had ground
truth; most judge deployments skip that step and inherit an unmeasured
failure rate.

The deploy rule compresses the whole slide: advisory first, veto only
with data. It also explains the capstone's architecture one more time —
judge_verdict is a display column in the approval queue, informing the
human at rung 3 rather than replacing them. Improving the judge's prompt
and re-measuring the agreement table is a lab stretch, and the exercise
generalizes: that loop — reword, re-measure — IS judge engineering.
-->

---

**The Verification Ladder · 6 of 7**

# M9.3.6 · Rung 3: The Human Gate

The top rung, and the enterprise non-negotiable:

```text
assistant drafts  ->  row: status=pending
                          |
advisor reviews rule + judge + note, decides
                          |
        approved  ->  client sees it
        rejected  ->  client never knows it existed
```

Nothing client-facing without a decision.

<!--
The human gate is what rungs 1 and 2 cannot be: a verifier whose
imagination is not bounded by prediction or training data. It catches
the wrong-but-compliant note, the tone that reads badly this week, the
fact that is technically true and commercially unwise. It costs the most
— real minutes from a licensed professional, a queue, latency measured
in hours — which is exactly why the cheaper rungs exist: they filter
what reaches the expensive one and brief it (the queue shows the rule
problems and the judge's opinion next to every draft).

In regulated industries this rung is not a design preference. Client
communications in finance carry review obligations; "the AI sent it" is
not a defense. The gate turns a compliance requirement into
architecture: pending → approved | rejected, decisions final, with a
reason recorded. Note what the gate consumes — the DRAFT framing M8
established. The assistant was never writing to clients; it was always
writing to this queue. That framing was today's seam.
-->

---

**The Verification Ladder · 7 of 7**

# M9.3.7 · Least Oversight That Works

Choose rungs by stakes, not by fashion:

```text
rules       always. every output, no exceptions
+ judge     volume high, rules can't be written,
            wrong answers survivable
+ human     a client will read it, money moves,
            or a regulator cares
```

Yesterday: least autonomy that works.
Today: least oversight that works. Same instinct.

<!--
The mirror of M8's closing rule is deliberate: "least autonomy that
works" sized how much freedom the model gets; "least oversight that
works" sizes how much checking its output gets. Both resist the same
two failure modes — under-engineering (shipping unchecked prose to
clients) and over-engineering (a human approving every spelling
correction, which guarantees the queue gets rubber-stamped).

The stacking logic reads top down: rules are free, so they are
unconditional. A judge earns its call when volume is high, the quality
being checked resists rules, and a wrong verdict is survivable — the
advisory-only rule from M9.3.5 standing. The human gate is reserved for
consequence: client-facing, money-moving, regulator-visible. The Chronos
advisor note trips the first condition, which is why the capstone build
runs all three rungs on every portfolio answer: free, advisory, final.
-->

---

<!-- _class: lead -->

**Shipping The Gate · 1 of 5**

# M9.4.1 · A Draft Is A Row

`advisor_note_drafts` — the gate, as a table:

```text
question, note, verdict, note_source,
review_problems, judge_verdict        the evidence
status   pending -> approved | rejected
decision_reason                       the human's why

only decide_note_draft may set "approved"
decisions are final — no un-approve
```

<!--
The state machine is three states and two transitions, and the
architecture guarantees both rules the compliance story needs. Every
column before status is evidence — everything the human needs to decide
sits in the row, including both lower rungs' verdicts (review_problems
from the rules, judge_verdict from the model). The decision columns
record who-said-what: status plus a mandatory reason.

The two invariants are enforced by construction, not convention.
Submission code writes pending unconditionally — there is no code path
from "assistant produced text" to "approved" that does not pass through
the decision function, and that function is the only writer of the
approved status (lab step 2 builds it; a test verifies it). Decisions
are final: deciding a decided draft raises a domain error (HTTP 409),
because an audit trail that can be silently rewritten is not an audit
trail. One function per file makes "the only code that can approve" a
greppable, reviewable claim — the business-readable naming rule paying
off as a security property.
-->

---

**Shipping The Gate · 2 of 5**

# M9.4.2 · Persistence For Free

```text
1. ask the assistant  ->  draft #7 pending
2. kill uvicorn           (the process dies)
3. restart the API
4. GET /advisor/drafts -> draft #7, still pending
```

No checkpoint framework. No resume logic.

**State that must survive is a row, not a variable.**

<!--
Frameworks sell persistence as a feature — checkpointers, thread state,
resume tokens. The capstone gets durable state with zero of that
machinery, because the design put the state that matters in the only
place that survives a process: the database. The pending draft is a row,
so a deploy, a crash, or a laptop reboot changes nothing about the
approval queue. The four-step sequence is runnable live and makes a
satisfying demo precisely because nothing visible was built for it.

The general design rule: decide which state must survive a restart, put
exactly that state in durable storage, and let everything else die with
the process. In this feature the conversation memory deliberately lives
in st.session_state — closing the browser tab forgets the chat, and
that is a defensible choice for a drafting tool — while the approval
queue, the thing with compliance weight, is durable. Choosing per piece
of state, rather than persisting everything or nothing, is the actual
skill. The miniature version is m9/state_resume.py: fifteen lines, a
JSON file, the same lesson.
-->

---

**Shipping The Gate · 3 of 5**

# M9.4.3 · The Wiring You Inherit

Given, working, yours to read — not to write:

```text
chat panel        POST /assistant   (+ history)
approval queue    GET  /advisor/drafts
approve button    POST /advisor/drafts/{id}/decision
Alice's dashboard GET  /messages    (approved only)
```

You write functions. The plumbing is done.

<!--
The M9 lab inverts the usual ratio: the UI and endpoints — normally the
time sink — ship complete, and the lab is only the four functions that
give them behavior. The chat panel keeps the transcript and sends it;
the queue panel renders every pending draft with its evidence and wires
Approve/Reject to the decision endpoint; the investor dashboard shows
approved notes and nothing else. Zero Streamlit gets written today.

The endpoints degrade honestly while the lab is unfinished, and the
degradation IS the progress meter: the queue endpoints work from day one
but stay empty until submit exists; the decision endpoint answers 501
naming the missing function; the assistant answers but with draft_id
null until the intake is written. Each implemented function visibly
turns on its own piece of UI. Reading the route code before writing the
functions is worth five minutes — it is the house pattern (role checks,
translate_domain_errors, function-level lab imports) that every Chronos
feature follows.
-->

---

**Shipping The Gate · 4 of 5**

# M9.4.4 · Guardrails You Already Have

Nothing new — an inventory of the week so far:

```text
input   router refuses trade-shaped questions
        before any tool runs
output  80-word cap, threshold must be cited
usage   ONE bounded redraft (max_turns thinking)
scope   advisor AI cannot mutate portfolios —
        it imports no trading function
```

Guardrails live at boundaries, visibly.

<!--
"Guardrails" as a topic tends to arrive as a new product category. This
slide reframes: the workflow already has input validation, output
validation, usage caps, and scope restriction — built across M7 and M8
under other names. The router refusing trades is an input guardrail that
runs before any capability is touched. The reviewer's rules are output
guardrails. The single bounded redraft is a usage cap, the same instinct
as max_turns. And the strongest one is structural: the assistant package
imports no trading function, so mutation is not refused, it is
impossible — the guardrail nobody can prompt-inject away.

The one addition worth noticing in the given code: the route layer caps
question and history length at the boundary, where the request enters.
That placement is the principle worth keeping — checks live where data
crosses a trust boundary, written as visible code, not sprinkled through
business logic. A reader should be able to find every guardrail by
reading the boundary files.
-->

---

**Shipping The Gate · 5 of 5**

# M9.4.5 · The Payoff, Live

One loop, two dashboards:

```text
advisor   ask -> draft #1 lands in the queue
advisor   read rule + judge + note -> Approve
switch    log in as alice@example.com
alice     "Messages From Your Advisor" — it's there

and the other path:
advisor   Reject (with reason)
alice     nothing. ever.
```

<!--
The full loop, end to end, on the feature built across two days: the M8
workflow routes, gathers, judges, drafts, and reviews; the M9 gate holds
the result as a pending row; a human decision publishes it to the one
audience that matters. The reject path is half the demo on purpose —
"Alice never sees it" is the property the entire ladder exists to
guarantee, and watching a rejected note simply not exist on the client
dashboard makes the guarantee concrete in a way no architecture diagram
can.

This moment is also the lab's finish line: with steps 1 and 2 done
(about the halfway mark of the hour), every participant can run exactly
this sequence with their own code in the loop. A useful thing to notice
at that moment: how much of the week is in this one round trip — M0's
business-readable functions, the point-in-time price rule under the
metrics, M7's loop discipline, M8's patterns, M9's gate. One feature,
every module load-bearing.
-->

---

# M9.5.1 · What Finishing Costs

Today's additions, priced:

```text
memory   ~20-25 tokens/turn, re-sent every turn
         (windowed: 135 -> 89 on six turns)
judge    +1 model call per draft
         bought: an opinion. measured: 2/6
human    minutes per draft + a queue
         bought: the only rung that catches
         what nobody predicted
```

<!--
The mirror of M8's "What A Step Costs," applied to finishing touches,
every number from this morning's measured runs. Memory is the quiet
compounding cost: 20-25 tokens per turn re-sent on every subsequent
turn means cost quadratic in conversation length until a window bounds
it — the reason bounding was a build step and not an optimization.

The judge line is deliberately unflattering: one extra call bought an
opinion whose measured agreement was 2/6. At frontier quality the same
call buys a much better opinion — but the pricing habit is the point:
name what the call costs and what it verifiably buys, per rung. The
human line inverts the accounting — by far the most expensive verifier,
and the only one whose coverage is unbounded. The cheaper rungs justify
themselves largely by how well they filter and brief this one. Sized
against yesterday's numbers, the whole ladder costs less than one
1,054-token framework system prompt per question — oversight is cheap
relative to autonomy.
-->

---

# M9.5.2 · Streaming, Briefly

Why chat UIs feel alive:

```python
streamer = TextIteratorStreamer(
    tokenizer, skip_prompt=True,
    skip_special_tokens=True)
Thread(target=model.generate, kwargs=dict(
    **inputs, streamer=streamer)).start()

for piece in streamer:
    print(piece, end="", flush=True)
```

Same tokens, sooner. `m9/streaming.py` runs it offline.

<!--
Streaming changes when tokens arrive, not what they say: generation is
sequential anyway, and a streamer hands each piece over the moment it
exists instead of after the last one. Perceived latency drops from
"the full generation time" to "time to first token," which is the
entire typing-effect illusion of every chat product. The snippet is the
real mechanism at transformers level — generate runs in a thread, the
streamer is an iterator the UI loop consumes.

The capstone deliberately does not stream, for a reason worth owning:
the template path — the no-model install that the feature must fully
support — produces its note instantly, so there is nothing to stream,
and an SSE endpoint plus a streaming Streamlit panel is FastAPI
plumbing, not agent engineering. The seam is already in place: the
draft function is the single swap point, so streaming (or a cloud
model) slots in behind it without touching the workflow. Wiring it is
a lab stretch.
-->

---

# M9.5.3 · The Day In One Picture

```text
M7  the loop, by hand      you own the runtime
M8  the workflow           patterns, least autonomy
M9  the finished feature   memory + ladder + gate

        remember   verify   gate
             \        |      /
      one assistant, in the product,
      behind a human decision
```

Tomorrow: its tools are still hardwired. **MCP.**

<!--
The three-day arc closes where Day 3 promised: what began as a
hand-written loop is now a product feature — conversational, verified
at three rungs, gated behind a human, live in both dashboards, durable
across restarts. Each day kept its one question: M7, how does an agent
actually work; M8, how do you compose one responsibly; M9, who checks
the work.

The bridge to Day 4 names the remaining limit precisely. Every tool
this assistant uses is a Python function hardwired into its own
codebase — gather_client_facts can never reach a CRM, a document store,
or any system Chronos does not own, and every new integration means
writing and shipping more adapter code. MCP is the standard that breaks
that coupling: tools become servers agents discover and call across
system boundaries. Day 4 connects this assistant to the world outside
its own repo.
-->

---

<!-- _class: lead -->

# M9.L1 · Lab: Everything You Built, Gated

60 minutes. Payoff at the halfway mark.

```text
step 1  submit_note_for_approval   the intake
step 2  decide_note_draft          the decision
        >>> the loop closes on screen <<<
step 3  answer_with_memory         the follow-up
stretch judge_note_with_model      rung 2
```

Build order ≠ deck order. **Gate first.**

<!--
The lab is one hour, so it is scoped payoff-first: the two gate
functions come before memory because they are the culmination — with
steps 1 and 2 done, the loop from M9.4.5 runs live with the
participant's own code deciding what Alice sees. Everything built this
week feeds that moment: their M8 router routes the question, their
verdict logic judges, their draft function writes, their reviewer
checks, and their M9 gate decides. Memory lands third, fixing the
M9.1.2 misroute in their own chat panel. The judge is a stretch: its
two tests sit skipped until the function exists, and the queue's judge
column shows a dash — nothing downstream depends on it.

No warm-up phase this time — the module's three experiments already ran
the m9 toys. The M9 tests and live UI use a compact M9-owned reference
assistant for yesterday's workflow, so an unfinished M8 lab does not
block today's gate. Participants who finished M8 can swap their own
workflow back in as a stretch after M9 is green.
-->

---

# M9.L2 · The Feature In One Picture

```text
GIVEN                          YOU
─────                          ───
chat panel + queue + messages  submit_note_for_approval
4 endpoints (routes ready)     decide_note_draft
advisor_note_drafts table      answer_with_memory
M8 reference assistant         judge_note_with_model
condense helper, queries
model loader (from M8)             (stretch)
```

Zero Streamlit. Zero SQL setup. Four functions.

<!--
The dividing line is drawn on one principle: participants write what M9
taught and inherit everything else. The UI panels, the endpoints, the
table, the windowing helper, and the read-side queries are plumbing —
necessary, but not today's lesson. The four functions are today's
lesson made executable: the gate's intake, the human decision, the
memory seam, and the optional judge.

Worth reading even though it is given: note_draft_queries.py, because
the client-visibility rule lives there in one place (approved status
filter), and submit and decide both return rows through its builder.
The given code is short on purpose — reading all of it takes ten
minutes and pays back in step 1, where the docstring hints reference
its names.
-->

---

# M9.L3 · The Interfaces You Implement

```python
def submit_note_for_approval(
    db, advisor_user_id, client_user_id,
    question, answer, judge_verdict=None,
) -> AdvisorNoteDraftResponse: ...

def decide_note_draft(
    db, advisor_user_id, draft_id,
    decision, reason,
) -> AdvisorNoteDraftResponse: ...

def answer_with_memory(
    db, client_user_id, question,
    conversation_history=None,
) -> AdvisorAssistantAnswerResponse: ...
```

Every stub's docstring carries the full hint list.

<!--
Three core signatures (the stretch judge is note, verdict in — YES, NO,
or None out). The types tell most of the story: submit consumes the M8
answer schema and produces a draft row response — the bridge between
yesterday's workflow and today's queue. Decide consumes an id and a
decision and is the only path to an approved status. Answer_with_memory
has exactly the signature M8's workflow had, plus a history that
finally does something — which is why the endpoint can call either
depending on whether history arrived.

The build discipline that makes the hour work: run the lab tests after
every function, not at the end —
uv run python -m pytest labs/m9_advisor_assistant -q — tests are
ordered by step, so the failure wall recedes file by file: 13 fail, then
10, then 7, then 0 (with 2 skips holding the stretch). The stub
docstrings name every helper needed, including the given builder and
status constants, so the functions are short — the reference solutions
are all under twenty lines.
-->

---

# M9.L4 · Success Criteria

```bash
cd CAPSTONE-PROJECT/chronos_wealth_management
uv run python -m pytest labs/m9_advisor_assistant -q
```

13 green (+2 stretch skips), and three moments:

```text
~min 25  ask -> queue -> Approve -> Alice sees it
         (Reject -> she never does)
restart  kill the API, relaunch: queue intact
memory   M9.1.2's follow-up now stays on thread
```

Shipped suite stays green: `uv run python -m pytest -q`

<!--
The meter is 15 tests: 13 grade the core steps in build order (gate,
HTTP round trip, M8 independence, memory), 2 sit skipped until the stretch judge exists.
The three named moments are the acceptance criteria that matter beyond
green — each one is a property of the system demonstrated, not
asserted: the visibility rule (approved only, rejection is silent),
durability (the queue is rows, not variables), and the thread-keeping
fix for the exact failure that opened the module.

Two mechanical notes that save debugging time. Always invoke pytest as
uv run python -m pytest — a bare uv run pytest can silently pick up a
PATH pytest (conda's, typically) with the wrong Python when the venv
and extras are out of sync. And the full shipped suite (70 tests) must
stay green throughout — the lab adds a feature; it never bends the
app's invariants to do it.
-->

---

# M9.L5 · Stretch Options

```text
1  the judge      implement it; 2 tests un-skip,
                  the queue's judge column lights up
2  judge, better  reword the prompt, re-run
                  m9/llm_judge.py — beat 2/6?
3  stream it      SSE endpoint + the chat panel
4  summarize      model fold instead of window;
                  what breaks in the tests?
5  read Day 4     list every hardwired tool here;
                  which would MCP externalize?
6  swap in M8     replace the reference assistant with
                  your completed M8 workflow
```

<!--
Ordered by payoff-per-minute. The judge is first because it completes
the ladder in the product — after it, the approval queue shows all
three rungs' opinions side by side on every draft, which is the
module's thesis rendered as UI. Judge-better is the same file plus
judge engineering: reword, re-measure, and watch how much the verdict
moves with the prompt — the agreement table turns prompt sensitivity
from a claim into a number.

Streaming is the plumbing-heaviest option and deliberately last among
the build items. The summarize stretch is quietly the most instructive
failure hunt: swapping the deterministic fold for a model summary
breaks the windowing test's determinism and can lose the very keywords
the router needs — the M9.2.3 lesson arriving as red tests. The Day 4
reading sets up tomorrow: gather_client_facts, the thresholds, the
price lookups — every one a hardwired in-process call today, every one
a candidate MCP server tomorrow.
-->
