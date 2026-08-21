"""One concept: send instruction, context and prompt to a model.

Try:
- Change 42% to 30%.
- Remove the policy context.
- Name which input caused the answer to change.
"""

from m2_smolm_setup import call_smolm


messages = [
    {"role": "system", "content": "Answer only from the supplied context."},
    {"role": "system", "content": "Context:\nPolicy: no holding may exceed 35%."},
    {"role": "user", "content": "Is AAPL too large at 42%?"},
]

reply = call_smolm(messages)

print("request:")
for message in messages:
    print(f"{message['role']:>9} -> {message['content']}")
print("\nmodel reply:", reply)
