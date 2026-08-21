"""One concept: the same prompt gets a different answer from different context.

Try:
- Change the permissive policy from 50% to 40%.
- Keep the question fixed.
- Identify which input owned the changed answer.
"""

from m2_smolm_setup import call_smolm


question = "Can Alice hold 42% of her account in AAPL?"
strict_context = "Policy: one holding may not exceed 35%."
permissive_context = "Policy: one holding may be up to 50%."
changed_context = "Policy: one holding may be up to 40%."

strict_messages = [
    {"role": "system", "content": "Answer only from the supplied context."},
    {"role": "system", "content": f"Context:\n{strict_context}"},
    {"role": "user", "content": question},
]
permissive_messages = [
    {"role": "system", "content": "Answer only from the supplied context."},
    {"role": "system", "content": f"Context:\n{permissive_context}"},
    {"role": "user", "content": question},
]
changed_messages = [
    {"role": "system", "content": "Answer only from the supplied context."},
    {"role": "system", "content": f"Context:\n{changed_context}"},
    {"role": "user", "content": question},
]

strict_reply = call_smolm(strict_messages)
permissive_reply = call_smolm(permissive_messages)
changed_reply = call_smolm(changed_messages)

print("same question:", question)
print("35% context ->", strict_reply)
print("50% context ->", permissive_reply)
print("40% context ->", changed_reply)
