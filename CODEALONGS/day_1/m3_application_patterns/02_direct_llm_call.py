"""One concept: a direct LLM call is messages in, reply out.

Try:
- Change the user message to a rewrite task.
- Remove the supplied portfolio fact.
- Notice that a direct call cannot know private facts you did not send.
"""

from m3_smolm_setup import call_smolm


messages = [
    {"role": "system", "content": "You are a concise advisor assistant."},
    {"role": "user", "content": "Explain the risk in a portfolio with 52% in AAPL."},
]
raw_reply = call_smolm(messages)
reply = raw_reply

rewrite_messages = [
    {"role": "system", "content": "You rewrite client notes in plain English."},
    {"role": "user", "content": "Rewrite: concentration exposure remains above policy tolerance."},
]
rewrite_reply = call_smolm(rewrite_messages)

print("messages:", messages)
print("reply:", reply)
print("rewrite reply:", rewrite_reply)
