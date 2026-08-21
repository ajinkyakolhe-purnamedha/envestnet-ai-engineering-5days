"""One concept: bound LlamaIndex memory before sending it to the model.

Try:
- Change TOKEN_LIMIT from 30 to 20.
- Add another older turn.
- Inspect which messages remain in memory.get().
"""

from llamaindex_closure_setup import ask_llamaindex, memory_buffer, message


TOKEN_LIMIT = 30


full_history = [
    message("user", "How is Alice doing overall?"),
    message("assistant", "Portfolio value is $104,120."),
    message("user", "Which holding is largest?"),
    message("assistant", "AAPL is 52% of the account."),
    message("user", "What is the concentration guideline?"),
    message("assistant", "One holding should stay below 35%."),
]
new_question = "Why is that a problem for Alice?"

memory = memory_buffer(full_history, token_limit=TOKEN_LIMIT)
windowed_history = memory.get()
prompt = "\n".join(str(item) for item in [*windowed_history, message("user", new_question)])
windowed_reply = ask_llamaindex(prompt, max_tokens=40)

print(f"full entries: {len(full_history)}")
print(f"windowed entries: {len(windowed_history)}")
print("windowed reply:", windowed_reply or "[no new text]")
