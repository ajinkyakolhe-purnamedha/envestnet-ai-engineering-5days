"""A small, logged boundary around a model response."""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reply_to_advisor(message: str, call_model: callable) -> str:
    """Return model text, or a safe message when no text is available."""
    reply = call_model(message)
    logger.info("model_reply_received=%s", bool(reply))
    return reply or "I could not produce an answer. Please try again."


print(reply_to_advisor("Name one portfolio risk.", lambda _: "AAPL is concentrated."))
