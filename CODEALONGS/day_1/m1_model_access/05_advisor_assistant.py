"""An advisor assistant: facts in, logged answer out."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)
os.environ.setdefault("HF_HUB_OFFLINE", "1")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("advisor")

MODELS = Path(__file__).resolve().parents[3] / "OFFLINE-AI-Models"

SYSTEM = (
    "You are a financial advisor's assistant. Answer using "
    "only the facts given. Never invent a number. Never "
    "give investment advice."
)

FACTS = {
    "client": "Alice",
    "cash_balance": 41250.00,
    "largest_holding": "AAPL",
    "largest_holding_pct": 52.0,
}


# #region assistant
def build_prompt(question: str, facts: dict) -> str:
    """Instruction + grounding facts + the question."""
    given = "\n".join(f"{k}: {v}" for k, v in facts.items())
    return (
        f"{SYSTEM}\n\nFacts:\n{given}"
        f"\n\nQuestion: {question}"
    )


def answer(question: str, facts: dict, call_model) -> str:
    """One turn across the boundary, both sides measured."""
    prompt = build_prompt(question, facts)
    log.info("prompt_chars=%d", len(prompt))
    reply = call_model(prompt)
    log.info("reply_chars=%d", len(reply))
    return reply
# #endregion


def hosted_backend():
    """Gemini. Needs a key, a network, and unspent quota."""
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    def call(prompt: str) -> str:
        reply = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )
        return reply.text

    return call


def local_backend():
    """The committed weights. Always available, much weaker."""
    from transformers import pipeline

    generate = pipeline(
        "text-generation",
        model=str(MODELS / "smollm2-135m-instruct"),
    )

    def call(prompt: str) -> str:
        out = generate(prompt, max_new_tokens=60)
        return out[0]["generated_text"][len(prompt):]

    return call


QUESTION = "How concentrated is this portfolio?"

try:
    log.info("backend=gemini-3.5-flash-lite")
    print(answer(QUESTION, FACTS, hosted_backend()))
except Exception as error:
    log.warning("hosted backend failed: %s", type(error).__name__)
    log.info("backend=smollm2-135m-instruct")
    print(answer(QUESTION, FACTS, local_backend()))
