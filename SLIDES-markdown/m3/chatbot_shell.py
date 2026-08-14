"""One chatbot shell. Swap the brain, not the product.

Fully offline shape demo. Run:
    uv run --project ../CODE-ALONGS \
        python m3/chatbot_shell.py
"""


def fake_model(messages: list[dict]) -> str:
    """Stand-in for any local or hosted chat model."""
    last = messages[-1]["content"]
    return f"MODEL_REPLY: I received '{last[:42]}...'"


# #region shell
SYSTEM = "You are a concise financial analyst."


def reply(message: str, history: list[dict]) -> str:
    messages = [{"role": "system", "content": SYSTEM}]
    messages += history
    messages.append({"role": "user", "content": message})
    return fake_model(messages)
# #endregion shell


if __name__ == "__main__":
    history = []
    answer = reply("Explain ETFs in one sentence.", history)
    print(answer)
    history += [{"role": "user", "content": "Explain ETFs."},
                {"role": "assistant", "content": answer}]
    print(reply("Now compare them to mutual funds.", history))

# The UI is not the hard part. Every chatbot is a loop
# that rebuilds messages from system + history + new
# user input. M2's rule is still true here: the model
# remembers nothing; your application resends history.
