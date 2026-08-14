"""Time the model tier, then judge whether it helped.

Fully offline shape demo. Run:
    uv run --project ../CODE-ALONGS \
        python m3/tier_timer.py
"""

import time


def call(model: str, prompt: str, max_tokens: int = 400) -> str:
    time.sleep({"fast": 0.01, "default": 0.02, "deep": 0.03}[model])
    return f"{model} answer to {prompt}. " * {"fast": 4,
                                             "default": 6,
                                             "deep": 8}[model]


# #region timer
def words_per_second(model: str, prompt: str) -> float:
    t0 = time.time()
    reply = call(model, prompt, max_tokens=400)
    dt = time.time() - t0
    return len(reply.split()) / dt
# #endregion timer


if __name__ == "__main__":
    prompt = "Summarise Alice's portfolio risk."
    for model in ["fast", "default", "deep"]:
        print(model, round(words_per_second(model, prompt), 1), "words/sec")

# Latency is a product feature. A slower tier must buy
# visible quality, not just a longer answer. Measure the
# speed and score the output before making it default.
