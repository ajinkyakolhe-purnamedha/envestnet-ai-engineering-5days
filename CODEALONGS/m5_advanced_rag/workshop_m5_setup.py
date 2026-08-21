"""Shared local setup for M5 LlamaIndex and RAGAS snippets."""

from __future__ import annotations

import sys
from pathlib import Path


M4_DIR = Path(__file__).resolve().parents[1] / "m4_building_rags"
sys.path.insert(0, str(M4_DIR))

from workshop_llamaindex_setup import POLICY_DIR, use_local_models  # noqa: E402


REFERENCE_ANSWER = "No. 42% is above the 35% single-asset limit."
REFERENCE_CONTEXT = (
    "# Concentration limit\n"
    "No single asset may exceed 35% of the portfolio.\n\n"
    "# Minimum cash\n"
    "A proposed action must leave at least $2,000 in cash.\n\n"
    "# Conservative high-risk restriction\n"
    "A conservative portfolio may not add a high-risk asset.\n\n"
    "# Human confirmation\n"
    "Every proposed action requires human confirmation before execution."
)
