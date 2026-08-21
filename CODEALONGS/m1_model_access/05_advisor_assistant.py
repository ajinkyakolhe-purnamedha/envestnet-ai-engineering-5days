"""One concept: an AI application boundary puts facts into a model call."""

import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger("advisor")

sys.path.insert(0, str(Path(__file__).resolve().parent))

from m1_smolm_setup import call_smolm

SYSTEM = "You are a financial advisor's assistant. Use only the supplied facts."
FACTS = {
    "client": "Alice",
    "cash_balance": 41250.00,
    "largest_holding": "AAPL",
    "largest_holding_pct": 52.0,
}
QUESTION = "How concentrated is this portfolio?"


def build_prompt(question: str, facts: dict[str, object]) -> str:
    given = "\n".join(f"{key}: {value}" for key, value in facts.items())
    return f"{SYSTEM}\n\nFacts:\n{given}\n\nQuestion: {question}"


def answer(question: str, facts: dict[str, object], call_model) -> str:
    prompt = build_prompt(question, facts)
    log.info("prompt_chars=%d", len(prompt))
    reply = call_model(prompt)
    log.info("reply_chars=%d", len(reply))
    return reply


prompt = build_prompt(QUESTION, FACTS)
reply = answer(QUESTION, FACTS, call_smolm)
print(reply)
print("\nPrompt sent to the model:")
print(prompt)
