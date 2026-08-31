"""One concept: a local LLM explains trusted Chronos portfolio facts."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from m9_memory_verification_hitl.chronos_offline import generate

portfolio = {"client": "Alice", "cash": 25_000, "holdings": ["SPY", "QQQ", "GLD"]}
history = [{"role": "user", "content": "What do I own?"}]
messages = [
    {"role": "system", "content": "You are an educational Chronos investor assistant. Use facts only."},
    {"role": "system", "content": f"Trusted portfolio: {portfolio}"},
    *history[-4:],
    {"role": "user", "content": "Explain why diversification matters here."},
]

reply = generate(messages, max_new_tokens=80)
print("Local LLM reply:", reply)
print("Messages sent:", len(messages))
