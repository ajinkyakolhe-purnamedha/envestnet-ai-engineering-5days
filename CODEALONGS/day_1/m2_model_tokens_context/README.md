# M2 · Model, Tokens and Context

M1 made a call to a model. This pack opens that one call just far enough to
inspect transcript growth, token usage, context limits, meaning vectors, and a
transparent cost estimate. Chronos portfolio data is the shared synthetic
example; the mechanics apply to any AI assistant or workflow.

Run from this directory with `uv run jupyter lab`. Each code-along's first
code cell executes its paired cookbook snippet with `run_path`; start there,
then answer the questions in the following cells. Provider credentials are not
needed. The optional local tokenizer needs the offline model material already
used in M0/M1.

| Cookbook snippet | Teaches one thing | Code-along then explores |
| --- | --- | --- |
| `01_messages_grow.py` | history grows in the application | stateless resend and growing transcript |
| `03_token_ids.py` | text becomes token IDs | chunking across text, code and names |
| `05_count_context.py` | estimate one request | instruction/history cost contribution |
| `07_trim_history.py` | retain valid recent turns | forgetting versus a written summary |
| `09_embedding_similarity.py` | compare meaning vectors | search three synthetic policy chunks |
| `11_instrument_reply.py` | estimate one call's cost | duration and cumulative cost |

The lab extends the M1 AI assistant reference implementation. It deliberately
does not introduce model routing, prompt-engineering depth, or RAG
implementation.
