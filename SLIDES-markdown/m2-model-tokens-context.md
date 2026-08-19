---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M2.0 · Model, Tokens & Context

M1 made a model call. Now inspect what that call contains, costs, and forgets
in any AI application.

- Measure the request before treating it as a black box
- Explain why a chat has no server-side memory
- Keep context useful and bounded
- Preview why embeddings matter in M4

<!--
This is engineering inspection, not transformer theory. Keep returning to the
M1's Chronos Portfolio Assistant is the shared reference implementation.
Learners should transfer the same mechanics to a support, document, or
operations assistant: every application must own the call around the model.
-->

---

# M2.1 · One call has named parts

```text
model        capability, speed and price
instruction  standing behaviour
context      everything the model can read this turn
history      application-owned prior turns
new message  this turn's task
usage        input/output metadata after the call
```

The application assembles the request. The model returns a completion and usage.

These parts are the same whether the feature is a portfolio assistant, support
copilot, document workflow, or internal operations tool.

M1 starting point: `CODEALONGS/day_1/m1_model_access/01_closed_model_call.py`

<!--
The provider API is not the lesson. Label the pieces a participant owns at
every provider boundary. Usage metadata is returned after a call; a pre-call
number is an estimate.
-->

---

# M2.1 · Context has a hard limit

```text
instruction + history + retrieved facts + tool results + new message
                              ↓
                        context window
```

Everything the model must read has to fit. The reply also has a maximum size.

- Small/local models: often thousands to low hundreds of thousands of tokens
- Gemini 2.5 Flash: 1,048,576 input tokens; 65,536 output tokens
- Limits differ by model and change
- Check the deployed model before shipping

<!--
Context is not merely chat history. It is the complete input: a system
instruction, the history we replay, any retrieved policy excerpts, tool output,
and this new question. A model cannot attend to input that does not fit.

Use precise language for provider contracts: some providers publish separate
input and output limits. The operational rule is still the same: reserve room
for the response and check the current model's documented limits. Gemini 2.5
Flash's 1,048,576 input-token and 65,536 output-token limits were verified in
August 2026; re-check them before delivery.
-->

---

# M2.1 · There is no conversation on the server

```python
messages = [{"role": "user", "content": "What do I hold?"}]
messages.append({"role": "assistant", "content": "SPY, QQQ and GLD."})
```

On the next turn, the application sends both messages again.

- History is application state
- Each later request grows unless you manage it
- This affects context and spend

Source: `CODEALONGS/day_1/m2_model_tokens_context/01_messages_grow.py`

<!--
Ask learners to trace the third request. Products create memory by resending
history, summaries, retrieved facts, or stored profiles—not by assuming that
the model secretly remembers the last API call.
-->

---

# M2.1 · Checkpoint: observe transcript growth

1. Which messages will the next request include?
2. Which part of that history is a product decision?
3. What would be lost if the oldest turn disappeared?

Code-along: `CODEALONGS/day_1/m2_model_tokens_context/02_messages_grow_code_along.ipynb`

<!-- **Instructor only:** ask for a concrete message list before naming it memory. -->

---

# M2.2 · Text becomes tokens and token IDs

```python
token_ids = tokenizer.encode("AAPL is 52% of the portfolio.")
print(token_ids)
print(f"{len(token_ids)} tokens")
```

A token is a model-specific text chunk: not a word and not a character.

Source: `CODEALONGS/day_1/m2_model_tokens_context/03_token_ids.py`

<!--
Exact counts depend on the tokenizer. The local open-model tokenizer makes the
mechanism visible; it is not another provider's invoice calculator. Point out
spaces, punctuation, ticker symbols, and uncommon names.
-->

---

# M2.2 · Next-token prediction explains fluent mistakes

```text
given tokens so far → score likely next tokens → append one → repeat
```

The model does not automatically look up a private policy, verify a current
number, or enforce a business limit. Good prose can still be unsupported.

<!--
This establishes why later patterns add context, validation, tools, and tests.
Do not turn this into a model-architecture lecture.
-->

---

# M2.2 · Checkpoint: counts are evidence, not guesses

Compare a ticker, a sentence, and one line of code.

- Which has more characters?
- Which has more tokens?
- Why can model families count the same text differently?

Code-along: `CODEALONGS/day_1/m2_model_tokens_context/04_token_ids_code_along.ipynb`

---

# M2.3 · Context is the whole input, not just the question

```python
prompt = "You are concise. AAPL is 52% of the portfolio. What is the risk?"
estimated_tokens = len(prompt.split())
```

Real input may also contain instructions, history, retrieved facts, and tool
results. Count all of it.

Source: `CODEALONGS/day_1/m2_model_tokens_context/05_count_context.py`

<!--
Separate a local estimate, a model-specific tokenizer count, and actual usage
metadata. Provider windows and prices change, so use a dated delivery example
when needed instead of permanent slide claims.
-->

---

# M2.3 · When context grows, make an explicit choice

| Choice | Keeps | Loses / risks |
| --- | --- | --- |
| Keep all | exact transcript | cost and context grow |
| Keep recent turns | current conversation | older facts disappear |
| Summarise older turns | compact story | detail can distort |
| Retrieve relevant facts | task evidence | needs a retrieval system |

Know what the application will forget, compact, or recover.

<!-- M4 implements retrieval. M2 supplies the decision vocabulary. -->

---

# M2.3 · Trim history without breaking the transcript

```python
retained = messages[-(keep_turns * 2):]
while retained and retained[0]["role"] == "assistant":
    retained.pop(0)
```

Recent context is useful only if it remains a valid conversation.

Source: `CODEALONGS/day_1/m2_model_tokens_context/07_trim_history.py`

<!--
A naive slice can start with an assistant answer to a question the model no
longer sees. The small function makes this policy observable and testable.
-->

---

# M2.3 · Checkpoint: make forgetting visible

1. Retain one turn.
2. Name a fact that disappears.
3. Add a short summary that preserves it.
4. State one detail the summary might lose.

Code-along: `CODEALONGS/day_1/m2_model_tokens_context/08_trim_history_code_along.ipynb`

---

# M2.4.1 · Every response spends a quality / latency / cost budget

```text
more capable model or more context
              ↓
often more useful output — and often more latency or cost
```

Start with the smallest capable boundary, measure the task, then justify a
change with evidence.

<!--
M1 introduced model boundaries; M2 supplies operating evidence. Model
catalogues, limits, and prices must be verified at delivery time.
-->

---

# M2.4.2 · IQ vs Size vs Cost

| Tier | Usually good for | Usually gives up |
| --- | --- | --- |
| Tiny / local | tagging, simple rewrite | hard reasoning |
| Small | supplied-context answers | complex judgement |
| Frontier | hard reasoning, tools | cost and latency |

```text
more capable model often buys better task performance
and usually costs more to run and wait for
```

Choose the smallest model that reliably passes the task's tests.

<!--
"IQ" is deliberately shorthand for task capability, not a universal property.
Model size is an imperfect proxy: architecture, data, post-training, reasoning
mode, and the supplied context all matter. Mixture-of-experts models make raw
parameter counts especially misleading.

The practical decision is not "what is the best model?" It is "what is the
smallest model that reliably completes this specific task under our quality,
latency, cost, and data-boundary constraints?" M3 supplies the pattern choice;
later evaluation modules supply the evidence.
-->

---

# M2.4.4 · Bigger Is Also Slower

**Where time goes**

- Time to first token: reading the input context
- Tokens per second: generating the reply
- Larger models and longer context can make both slower
- Thinking modes may spend extra tokens before answering

**What helps:** send less context, choose a smaller capable tier, cache stable
prefixes, or stream the answer. Streaming improves perceived wait—not total work.

<!--
Separate the two latency problems. Time to first token is dominated by how much
input the model must read; sending less context helps. Generation speed is more
dependent on the selected model tier; a smaller capable model helps there.

Streaming is a user-experience improvement. It shows partial output sooner but
does not make the model generate the complete answer faster. This is why M2
measures duration and why M3 asks for the least-complex sufficient pattern.
-->

---

# M2.4.5 · Instrument one call transparently

```python
def estimate_cost(input_tokens, output_tokens, input_rate, output_rate):
    return input_tokens / 1_000 * input_rate + output_tokens / 1_000 * output_rate
```

Record token usage, duration, and cumulative cost beside the feature.

Source: `CODEALONGS/day_1/m2_model_tokens_context/11_instrument_reply.py`

<!--
Rates are injected into this example rather than treated as permanent facts.
In production record model name, time, input/output usage, duration, and rate
version used for an estimate.
-->

---

# M2.5 · Embeddings are vectors for meaning

```python
similarity = cosine(concentration_risk, large_single_holding)
```

An embedding maps text to numbers so related meanings are near each other.
It can find “single large holding” for a “concentration risk” query. It does
not prove the text is current, complete, or correct.

Source: `CODEALONGS/day_1/m2_model_tokens_context/09_embedding_similarity.py`

---

# M2.5 · Checkpoint: similarity is not truth

Rank three synthetic policy chunks against a query vector.

- Which chunk is most related?
- What evidence would a user still need?
- Which later module builds retrieval as an application system?

Code-along: `CODEALONGS/day_1/m2_model_tokens_context/10_embedding_similarity_code_along.ipynb`

<!-- Answer: M4. Embeddings are a mechanism; retrieval needs data preparation, citations, and evaluation. -->

---

# M2.L · Mini lab: measure one synthetic reply

Given supplied usage metadata, print input tokens, output tokens, and a
transparent estimated cost. No provider key or live request is required.

Source: `CODEALONGS/day_1/m2_model_tokens_context/lab/mini_lab.py`

---

# M2.L · Main lab: instrument the M1 assistant

Extend the M1 AI assistant reference implementation—the synthetic Chronos
assistant—and do not build a new chatbot.

1. Show per-call and cumulative cost.
2. Trim history and demonstrate deliberate forgetting.
3. Record one quality / cost / latency observation.
4. Keep tests offline.

Lab pack: `CODEALONGS/day_1/m2_model_tokens_context/lab/`

<!-- **Instructor only:** timebox to 60–90 minutes. Release the solution after groups explain one trim and one accumulated-cost calculation. -->

---

<!-- _class: lead -->

# M2.6 · You can now inspect a call

M1: what models can do and where they run.
M2: what one call contains, costs, and forgets.
M3: what application pattern earns its added complexity.

These mechanics apply to every AI workflow; Chronos is simply the shared
synthetic example.

Next question: when is a direct call enough—and when must the application add
structure, facts, learned behaviour, or dynamic steps?
