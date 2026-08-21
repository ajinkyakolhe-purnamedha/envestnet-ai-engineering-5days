"""Instructor solution for the terminal-first Chronos Portfolio Assistant."""

import logging
from collections.abc import Callable

SYSTEM = "You are Chronos's portfolio assistant. Be brief and factual."
logger = logging.getLogger(__name__)


def build_messages(message: str, history: list[dict[str, str]]) -> list[dict[str, str]]:
    """Build the complete transcript sent with the current turn."""
    return [{"role": "system", "content": SYSTEM}, *history, {"role": "user", "content": message}]


def reply(
    message: str,
    history: list[dict[str, str]],
    call_model: Callable[[list[dict[str, str]]], str],
) -> str:
    """Call the selected model and return a safe learner-facing response."""
    answer = call_model(build_messages(message, history))
    logger.info("model_reply_received=%s", bool(answer))
    return answer or "I could not produce an answer. Please try again."
