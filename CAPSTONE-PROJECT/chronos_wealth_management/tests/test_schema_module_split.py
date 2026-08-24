"""Checks for the domain-oriented API schema modules."""

import chronos.api_schemas_advisor as advisor_schemas

from chronos.api_schemas_advisor import AdvisorAssistantAnswerResponse
from chronos.api_schemas_investor import PortfolioResponse, TradeRequest
from chronos.api_schemas_system import DemoResetResponse, LoginRequest


def test_split_schema_modules_export_expected_models():
    trade = TradeRequest(user_id=1, symbol="AAPL", side="BUY", amount=100.0)

    assert trade.symbol == "AAPL"
    assert PortfolioResponse.__name__ == "PortfolioResponse"
    assert AdvisorAssistantAnswerResponse.__name__ == "AdvisorAssistantAnswerResponse"
    assert LoginRequest(email="alice@example.com").email == "alice@example.com"
    assert DemoResetResponse(accounts_reset=1).accounts_reset == 1


def test_advisor_schema_module_excludes_retired_preview_models():
    for model_name in (
        "AdvisorPreviewAskRequest",
        "AdvisorPreviewReplyResponse",
        "TradeIntentPreviewRequest",
        "TradeIntentPreviewResponse",
    ):
        assert not hasattr(advisor_schemas, model_name)
