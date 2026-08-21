---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M2.0 · Model, Tokens & Context

M1 made a model call. M2 shows what a multi-turn AI application sends to the
model, how the reply changes, and what that call costs.

- Send instruction, context and prompt to a model
- Resend history on the next turn
- Change context and watch the answer change
- Count the growing multi-turn request
- Compare Cost / latency / model size across model tiers
- Preview token IDs and embedding search for M4

<!--
Lead with behaviour, then measurement. Students should first see the model
reply to a request. Only then do token counts and cost estimates have a reason.
-->

---

# M2.1 · A Single Turn Has Parts

```text
instruction  how the model should behave
context      facts the model may use now
prompt       the user's current task
reply        the model output
```

The application assembles the request. The model only sees what is sent in this
turn.

M1 starting point: `CODEALONGS/m1_model_access/05_advisor_assistant.py`

---

# M2.1 · Send The First Request

```python
messages = [
    {"role": "system", "content": "Answer only from the supplied context."},
    {"role": "system", "content": "Context:\nPolicy: no holding may exceed 35%."},
    {"role": "user", "content": "Is AAPL too large at 42%?"},
]

reply = call_smolm(messages)
```

Source: `CODEALONGS/m2_model_tokens_context/01_single_turn_call.py`

<!--
This calls the local SmolLM model so learners see real generated output while
the run still works offline.
-->

---

# M2.1 · Checkpoint: Change One Input

1. Change `42%` to `30%`.
2. Remove the policy context.
3. Ask the same question again.
4. Name which input caused the answer to change.

Try it in: `CODEALONGS/m2_model_tokens_context/01_single_turn_call.py`

---

# M2.2 · There Is No Conversation On The Server

Turn two is not magic memory. The application resends the prior user and
assistant messages.

```python
turn_two_messages = [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "What do I hold?"},
    {"role": "assistant", "content": "You hold AAPL and SPY."},
    {"role": "user", "content": "Is that too much?"},
]
```

Source: `CODEALONGS/m2_model_tokens_context/02_multiturn_history_resend.py`

---

# M2.2 · Checkpoint: Remove The History

1. Keep only the latest user message.
2. Ask `Is that too much?`
3. Explain why `that` becomes ambiguous.
4. Decide which history the application must resend.

Try it in: `CODEALONGS/m2_model_tokens_context/02_multiturn_history_resend.py`

---

# M2.3 · Context Changes The Answer

Same question. Different supplied policy. Different answer.

```text
35% context -> No. AAPL at 42% violates the supplied 35% policy.
50% context -> Yes. AAPL at 42% is within the supplied 50% policy.
```

Source: `CODEALONGS/m2_model_tokens_context/03_context_changes_answer.py`

<!--
This is the bridge to RAG: the application can change the answer by changing
what facts the model can see. M4 retrieves those facts instead of hand-writing
them.
-->

---

# M2.3 · Checkpoint: Same Prompt, New Context

1. Keep the question fixed.
2. Change only the policy text.
3. Re-run the model call.
4. Identify whether the failure belongs to model behaviour or supplied context.

Try it in: `CODEALONGS/m2_model_tokens_context/03_context_changes_answer.py`

---

# M2.4 · Context Has A Hard Limit

```text
instruction + history + supplied context + new prompt
                              ↓
                        context window
```

Everything the model must read has to fit. Multi-turn calls grow because the
application resends prior turns.

---

# M2.4 · Count The Growing Request

```python
from litellm import token_counter

token_counter(model="gpt-4o-mini", messages=turn_one)
token_counter(model="gpt-4o-mini", messages=turn_two)
token_counter(model="gpt-4o-mini", messages=turn_three)
```

Source: `CODEALONGS/m2_model_tokens_context/04_count_multiturn_tokens.py`

---

# M2.4 · Checkpoint: Add One Turn

1. Add another assistant/user pair.
2. Count again.
3. Name what grew: instruction, history, context, or prompt.
4. Decide what the application should keep, summarize, or retrieve.

Try it in: `CODEALONGS/m2_model_tokens_context/04_count_multiturn_tokens.py`

---

# M2.5 · Cost / Latency / Model Size

| Tier | Usually buys | Usually costs |
| --- | --- | --- |
| Small | cheap supplied-context answers | less hard reasoning |
| Intermediate | stronger instruction following | more spend and wait |
| Large | highest capability target here | highest cost and latency target |

Choose the smallest model that reliably passes the task's tests.

---

# M2.5 · Price The Same Conversation

```python
from tokencost import calculate_cost_by_tokens

small_cost  = price(messages, "gpt-4o-mini")
medium_cost = price(messages, "gpt-4.1")
large_cost  = price(messages, "gpt-4o")
```

Source: `CODEALONGS/m2_model_tokens_context/05_cost_same_conversation.py`

<!--
The conversation stays fixed. Only model choice changes. That is why model
selection is a product economics decision, not a benchmark hobby.
-->

---

# M2.5 · Checkpoint: Same Conversation, New Model

1. Hold the conversation fixed.
2. Double expected output tokens.
3. Recompute one model's cost.
4. Decide what evidence would justify escalating model tier.

Try it in: `CODEALONGS/m2_model_tokens_context/05_cost_same_conversation.py`

---

# M2.6 · Text Becomes Token IDs

```text
"AAPL concentration risk"
        ↓
tokenizer
        ↓
[32, 146138, 27748, 7031]
```

Token IDs are model-specific identifiers. They are not embeddings yet.

Source: `CODEALONGS/m2_model_tokens_context/06_text_to_token_ids.py`

---

# M2.6 · Checkpoint: Tokens Are Not Words

1. Encode a ticker.
2. Encode a sentence.
3. Compare character count with token count.
4. Explain why provider usage metadata matters.

Try it in: `CODEALONGS/m2_model_tokens_context/06_text_to_token_ids.py`

---

# M2.7 · Embeddings Enable Meaning Search

```python
score = cosine(query_embedding, policy_embedding)
```

For meaning search, compare vectors rather than strings. A concentration-risk
question can sit near a concentration-limit policy even when the wording is not
identical.

Source: `CODEALONGS/m2_model_tokens_context/07_vectors_for_meaning_search.py`

---

# M2.7 · Checkpoint: Similarity Is Not Truth

1. Compare a query vector with three policy vectors.
2. Add another policy vector.
3. Explain why similar is not the same as true.
4. Carry this into M4: what should the model see before answering?

Try it in: `CODEALONGS/m2_model_tokens_context/07_vectors_for_meaning_search.py`

---

# M2.L · Mini Lab: Budget One Assistant Turn

Run the supplied conversation across three model choices.

```bash
cd CODEALONGS/m2_model_tokens_context
uv run python lab/mini_lab.py
```

Source: `CODEALONGS/m2_model_tokens_context/lab/mini_lab.py`

---

# M2.L · Main Lab: Inspect A Multi-Turn Assistant

Complete the lab pack:

1. Send a single-turn request.
2. Add history and observe the second turn.
3. Count and price the same conversation.
4. Remove history or context and name what the assistant loses.

Lab pack: `CODEALONGS/m2_model_tokens_context/lab/`

---

# M2.8 · You Can Now Inspect A Call

You can now answer:

- What did the application send?
- Why did turn two work?
- Which context changed the answer?
- How large and expensive was the request?
- Which vectors could retrieve context for M4?

M3 uses this discipline to choose the least-complex reliable application
pattern.
