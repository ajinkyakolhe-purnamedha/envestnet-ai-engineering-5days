"""Main lab starter: build a terminal-first portfolio assistant."""

SYSTEM = "You are Chronos's portfolio assistant. Be brief and factual."


def build_messages(message: str, history: list[dict[str, str]]) -> list[dict[str, str]]:
    """Build the complete transcript that an AI model needs for this turn."""
    return [{"role": "system", "content": SYSTEM}, *history, {"role": "user", "content": message}]


def reply(message: str, history: list[dict[str, str]], call_model: callable) -> str:
    """TODO: call the model with build_messages and handle an empty answer safely."""
    raise NotImplementedError("Implement this after completing the mini lab.")
