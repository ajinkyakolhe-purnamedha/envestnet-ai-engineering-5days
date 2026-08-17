"""Consistent logging setup for the local demo."""

import logging


def configure_logging() -> None:
    """Configure readable INFO logs for the local application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
