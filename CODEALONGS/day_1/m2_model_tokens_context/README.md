# M2 · Model, Tokens and Context

M2 starts with actual model-call behavior, then measures the consequences. The
application sends instruction, history, context, and prompt; the model replies;
the next turn resends prior turns; context changes the answer; then tokens,
cost, model tier, token IDs, and embeddings become inspectable.

Each snippet is self-contained and has a short `Try:` block at the top. Run the
file first, then change the named variable or message directly in the same
file. The first three snippets call local SmolLM; provider credentials are not
needed.

| Cookbook snippet | Teaches one thing | Code-along then explores |
| --- | --- | --- |
| `01_single_turn_call.py` | send instruction, context and prompt to local SmolLM | change context and prompt |
| `02_multiturn_history_resend.py` | turn two works because the app resends turn one | remove history and observe ambiguity |
| `03_context_changes_answer.py` | same question, different context, different answer | change only the supplied policy |
| `04_count_multiturn_tokens.py` | multi-turn calls grow because history is resent | add turns and count again |
| `05_cost_same_conversation.py` | the same conversation costs different amounts by model | project cost at product scale |
| `06_text_to_token_ids.py` | text becomes model-specific token IDs | compare text, tokens and token counts |
| `07_vectors_for_meaning_search.py` | embedding vectors enable meaning search | name why similarity is not truth |

The lab asks participants to inspect and budget a multi-turn Chronos assistant
without making a provider call. M4 turns the embedding-search preview into a
retrieval system.
