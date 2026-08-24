"""M9 lab test setup: app fixtures, template path, and controlled answers.

Importing * from tests.conftest brings the isolated database, seeded
demo users, and fixture prices. The autouse fixture pins the template
path. The ``canned_assistant`` fixture replaces the assistant call with
deterministic answers for tests that need exact routes, while the app
itself also has an M9-owned reference assistant so an unfinished M8 lab
does not block today's work.
"""

import pytest

from tests.conftest import *  # noqa: F401,F403

from chronos.api_schemas_advisor import (
    AdvisorAssistantAnswerResponse,
)

from labs.m8_advisor_assistant import (
    answer_client_question as m8_answer_module,
)
from labs.m8_advisor_assistant import model_loading as m8_model_loading
from labs.m9_advisor_assistant import answer_with_memory as memory_module
from labs.m9_advisor_assistant import (
    judge_note_with_model as judge_module,
)
from labs.m9_advisor_assistant import model_loading as m9_model_loading

_TRADE_WORDS = ("buy", "sell", "liquidate", "dump", "cash out", "trade")
_POLICY_WORDS = ("policy", "guideline", "rule", "threshold", "limit")


def canned_answer_client_question(
    db, client_user_id, question, conversation_history=None
):
    text = question.lower()
    if any(word in text for word in _TRADE_WORDS):
        return AdvisorAssistantAnswerResponse(
            route="trade", refused=True, verdict=None,
            note="Refused: the advisor assistant does not trade.",
            note_source="template", review_problems=[], metrics=None,
        )
    if any(word in text for word in _POLICY_WORDS):
        return AdvisorAssistantAnswerResponse(
            route="policy", refused=False, verdict=None,
            note="Guidelines: 35% concentration cap, 40% cash cap.",
            note_source="template", review_problems=[], metrics=None,
        )
    return AdvisorAssistantAnswerResponse(
        route="portfolio", refused=False, verdict="within guidelines",
        note="The portfolio is within guidelines.",
        note_source="template", review_problems=[], metrics=None,
    )


@pytest.fixture(autouse=True)
def force_template_notes(monkeypatch):
    monkeypatch.setattr(
        m8_model_loading, "load_offline_language_model", lambda: None
    )
    monkeypatch.setattr(
        m9_model_loading, "load_offline_language_model", lambda: None
    )
    monkeypatch.setattr(
        judge_module, "load_offline_language_model", lambda: None
    )
    yield


@pytest.fixture()
def canned_assistant(monkeypatch):
    monkeypatch.setattr(
        m8_answer_module,
        "answer_client_question",
        canned_answer_client_question,
    )
    monkeypatch.setattr(
        memory_module,
        "answer_client_question_for_m9",
        canned_answer_client_question,
    )
    yield canned_answer_client_question
