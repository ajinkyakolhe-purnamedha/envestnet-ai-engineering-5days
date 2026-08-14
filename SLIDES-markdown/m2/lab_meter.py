"""Lab: add a meter to the chatbot you already wrote.

Run:
    uv run --project ../CODE-ALONGS \
        python m2/lab_meter.py
"""

from chronos_offline import count_tokens

# Published prices per 1M tokens for the model you call.
PRICE_IN, PRICE_OUT = 5.00, 25.00

spent = 0.0


def metered_reply(messages: list[dict], answer: str) -> str:
    global spent

    sent = sum(count_tokens(m["content"]) for m in messages)
    got = count_tokens(answer)
    spent += sent / 1e6 * PRICE_IN + got / 1e6 * PRICE_OUT

    print(f"{sent} in, {got} out, ${spent:.5f} total")
    return answer


history = [{"role": "user", "content": "What do I hold?"}]
metered_reply(history, "AAPL, MSFT and GLD.")
history += [
    {"role": "assistant", "content": "AAPL, MSFT and GLD."},
    {"role": "user", "content": "Which is largest?"},
]
metered_reply(history, "AAPL, at 52% of the book.")

# Lesson: the second call costs more even though the user
# typed less. The whole message history is sent again.
