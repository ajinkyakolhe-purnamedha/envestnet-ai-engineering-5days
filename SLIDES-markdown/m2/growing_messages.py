"""There is no conversation on the server.

Run:
    uv run --project ../CODE-ALONGS \
        python m2/growing_messages.py
"""

messages = []


def turn(question: str, answer: str) -> None:
    messages.append({"role": "user", "content": question})
    # ... the model call goes here, with ALL of messages ...
    messages.append({"role": "assistant", "content": answer})
    print(f"sent {len(messages)} messages this turn")


turn("What do I hold?", "AAPL, MSFT and GLD.")     # sent 2
turn("Which is largest?", "AAPL, at 52%.")         # sent 4
turn("Is that risky?", "Yes. Concentrated.")       # sent 6

# Turn 3 resent turns 1 and 2. You paid for them again.
# "Memory" is just you resending the whole transcript.
#
# Nothing on the other end remembers you between calls.
# Statelessness is not a limitation to work around --
# it is the reason the same endpoint can serve everyone.
