"""One concept: each reply is appended to application-owned history."""

messages = [{"role": "user", "content": "What do I hold?"}]
messages.append({"role": "assistant", "content": "SPY, QQQ and GLD."})

print(f"Next request sends {len(messages)} messages.")
