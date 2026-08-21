"""One concept: LlamaIndex memory is messages the app sends again.

Try:
- Compare the reply with and without history.
- Remove the assistant's previous answer.
- Print memory.get_all() and inspect the stored transcript.
"""

from llamaindex_closure_setup import ask_llamaindex, memory_buffer, message


new_question = "Why is that a problem for Alice at 52%?"

empty_memory = memory_buffer([])
conversation_memory = memory_buffer([
    message("user", "What is the concentration limit?"),
    message("assistant", "The concentration limit is 35%."),
])

without_memory_messages = [*empty_memory.get(), message("user", new_question)]
with_memory_messages = [*conversation_memory.get(), message("user", new_question)]

without_memory_prompt = "\n".join(str(item) for item in without_memory_messages)
with_memory_prompt = "\n".join(str(item) for item in with_memory_messages)

without_memory_reply = ask_llamaindex(without_memory_prompt, max_tokens=48)
with_memory_reply = ask_llamaindex(with_memory_prompt, max_tokens=48)

print("without memory:", without_memory_reply or "[no new text]")
print("with memory:", with_memory_reply or "[no new text]")
