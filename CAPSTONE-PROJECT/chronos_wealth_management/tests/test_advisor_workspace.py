"""Advisor analysis, reports, and the advisor/investor boundary."""

from datetime import date

import pytest

from chronos.advisor_analysis_reports_and_client_lists import (
    analyze_client_portfolio,
    build_advisor_recommendations,
)
from chronos.advisor_analysis_reports_and_client_lists import generate_advisor_review_report, list_clients_for_advisor
from chronos.investor_trade_execution_and_preview import execute_investor_trade
from chronos.investor_accounts_portfolios_and_history import build_current_portfolio_snapshot
from chronos.api_schemas_investor import TradeRequest
from chronos.application_errors_and_permissions import WrongRoleError


def test_list_clients_requires_advisor_role(db, alice):
    with pytest.raises(WrongRoleError):
        list_clients_for_advisor(db, alice.id)


def test_list_clients_returns_investors(db, advisor):
    clients = list_clients_for_advisor(db, advisor.id)
    assert len(clients) == 1
    assert clients[0].client_email == "alice@example.com"
    assert all(client.total_value == pytest.approx(100_000.0) for client in clients)


def test_empty_portfolio_recommends_starting_allocation(db, alice_account):
    portfolio = build_current_portfolio_snapshot(db, alice_account)
    recommendations = build_advisor_recommendations(portfolio)
    assert any("Starting allocation" in text for text in recommendations)
    assert any("High cash" in text for text in recommendations)


def test_concentrated_portfolio_triggers_warnings(db, alice, alice_account):
    execute_investor_trade(
        db,
        alice_account,
        TradeRequest(user_id=alice.id, symbol="AAPL", side="BUY", amount=50_000.0),
    )
    portfolio = build_current_portfolio_snapshot(db, alice_account)
    metrics = analyze_client_portfolio(portfolio)
    assert metrics.largest_position_symbol == "AAPL"
    assert metrics.largest_position_ratio == pytest.approx(0.5)

    recommendations = build_advisor_recommendations(portfolio)
    assert any("Concentration risk" in text for text in recommendations)
    assert any("Low diversification" in text for text in recommendations)


def test_negative_return_triggers_performance_review(db, alice, alice_account):
    execute_investor_trade(
        db,
        alice_account,
        TradeRequest(user_id=alice.id, symbol="MSFT", side="BUY", amount=50_000.0),
    )
    alice_account.simulated_date = date(2020, 7, 6)  # MSFT 196 -> 191

    portfolio = build_current_portfolio_snapshot(db, alice_account)
    assert portfolio.total_return_percentage < 0
    recommendations = build_advisor_recommendations(portfolio)
    assert any("Performance review" in text for text in recommendations)


def test_report_uses_client_simulated_date(db, alice, advisor, alice_account):
    alice_account.simulated_date = date(2020, 7, 6)
    report = generate_advisor_review_report(db, advisor.id, alice.id)
    assert report.simulated_date == date(2020, 7, 6)
    assert report.advisor_user_id == advisor.id
    assert report.client_user_id == alice.id
    assert "2020-07-06" in report.summary


def test_report_rejects_non_advisor(db, alice):
    with pytest.raises(WrongRoleError):
        generate_advisor_review_report(db, alice.id, alice.id)


def test_advisor_cannot_trade_for_clients(client, advisor):
    response = client.post(
        "/trades",
        json={"user_id": advisor.id, "symbol": "AAPL", "side": "BUY", "amount": 1000.0},
    )
    assert response.status_code == 403

def test_report_for_unknown_client_is_not_found(db, advisor):
    from chronos.application_errors_and_permissions import RecordNotFoundError

    with pytest.raises(RecordNotFoundError):
        generate_advisor_review_report(db, advisor.id, 999)


def test_best_and_worst_holdings_identified(db, alice, alice_account):
    execute_investor_trade(
        db,
        alice_account,
        TradeRequest(user_id=alice.id, symbol="AAPL", side="BUY", amount=10_000.0),
    )
    execute_investor_trade(
        db,
        alice_account,
        TradeRequest(user_id=alice.id, symbol="MSFT", side="BUY", amount=10_000.0),
    )
    alice_account.simulated_date = date(2020, 7, 6)  # AAPL 108->118, MSFT 196->191

    metrics = analyze_client_portfolio(
        build_current_portfolio_snapshot(db, alice_account)
    )
    assert metrics.best_holding_symbol == "AAPL"
    assert metrics.best_holding_gain_loss > 0
    assert metrics.worst_holding_symbol == "MSFT"
    assert metrics.worst_holding_gain_loss < 0
