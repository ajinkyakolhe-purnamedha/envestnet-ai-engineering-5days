"""One concept: turn two works because the app resends turn one.

Try:
- Remove the assistant's first reply from turn two.
- Ask "Is that too much?" again.
- Explain why "that" is now ambiguous.
"""

from m2_smolm_setup import call_smolm


turn_one_messages = [
    {"role": "system", "content": "Answer from the conversation. Portfolio facts: Alice holds AAPL and SPY."},
    {"role": "user", "content": "What do I hold?"},
]
turn_one_reply = call_smolm(turn_one_messages)

turn_two_messages = [
    {"role": "system", "content": "Answer from the conversation. Policy: no holding may exceed 35%."},
    {"role": "user", "content": "What do I hold?"},
    {"role": "assistant", "content": turn_one_reply},
    {"role": "user", "content": "Is that too much?"},
]
turn_two_reply = call_smolm(turn_two_messages)

ambiguous_turn_two = [turn_two_messages[0], turn_two_messages[-1]]
ambiguous_reply = call_smolm(ambiguous_turn_two)

print("turn 1 reply:", turn_one_reply)
print("\nturn 2 request resends:")
for message in turn_two_messages:
    print(f"{message['role']:>9} -> {message['content']}")
print("\nturn 2 reply:", turn_two_reply)
print("without history:", ambiguous_reply)
