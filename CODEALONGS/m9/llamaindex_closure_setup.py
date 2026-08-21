"""Shared LlamaIndex setup for M9 product-closure snippets."""

from __future__ import annotations

import sys
from pathlib import Path

M4_DIR = Path(__file__).resolve().parents[1] / "m4"
M8_DIR = Path(__file__).resolve().parents[1] / "m8"
sys.path.insert(0, str(M4_DIR))
sys.path.insert(0, str(M8_DIR))

from llama_index.core import Settings  # noqa: E402
from llama_index.core.llms import ChatMessage  # noqa: E402
from llama_index.core.memory import ChatMemoryBuffer  # noqa: E402
from workshop_framework_setup import (  # noqa: E402
    QUESTION,
    check_guideline,
    draft_advisor_note,
    get_current_price,
    get_portfolio_allocation,
)
from workshop_llamaindex_setup import use_local_models  # noqa: E402


use_local_models()


def ask_llamaindex(prompt: str, max_tokens: int = 64) -> str:
    return Settings.llm.complete(prompt, max_tokens=max_tokens).text.strip()


def message(role: str, content: str) -> ChatMessage:
    return ChatMessage(role=role, content=content)


def memory_buffer(messages: list[ChatMessage], token_limit: int = 256) -> ChatMemoryBuffer:
    return ChatMemoryBuffer.from_defaults(chat_history=messages, token_limit=token_limit)


def m8_workflow_draft(question: str = QUESTION) -> dict:
    price = get_current_price("AAPL")
    allocation = get_portfolio_allocation("Alice", "AAPL")
    guideline = check_guideline("AAPL", 36.0)
    note = draft_advisor_note(price, allocation, guideline)
    return {
        "question": question,
        "facts": [price, allocation, guideline],
        "draft": note["note"],
        "allowed": note["allowed"],
        "evidence": note["evidence"],
    }
