"""Functions and logging. Never print() in real code.

Run:
    uv run --project ../CODE-ALONGS \
        python m0/functions.py
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
)
log = logging.getLogger("chronos.portfolio")


def position_value(shares: float, close: float) -> float:
    """What one holding is worth. Raises on bad input."""
    if shares < 0 or close <= 0:
        raise ValueError(f"bad position: {shares} @ {close}")

    value = round(shares * close, 2)
    log.info("value: %g x %.2f -> %.2f", shares, close, value)
    return value


if __name__ == "__main__":
    position_value(100, 80.46)
