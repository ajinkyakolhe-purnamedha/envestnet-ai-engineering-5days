"""One concept: retain recent complete turns without assistant-leading history."""


def trim_history(messages: list[dict[str, str]], keep_turns: int) -> list[dict[str, str]]:
    """Keep the most recent messages, correcting a retained assistant-leading slice."""
    retained = messages[-(keep_turns * 2) :]
    while retained and retained[0]["role"] == "assistant":
        retained.pop(0)
    return retained


history = [
    {"role": "user", "content": "What do I hold?"},
    {"role": "assistant", "content": "SPY, QQQ and GLD."},
    {"role": "user", "content": "Which is largest?"},
    {"role": "assistant", "content": "SPY at 52%."},
    {"role": "user", "content": "Is that concentrated?"},
]
print(trim_history(history, keep_turns=1))
