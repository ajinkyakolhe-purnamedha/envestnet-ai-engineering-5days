"""Advisor client access and the advisor/investor boundary."""

import pytest

from chronos.advisor_client_lists import list_clients_for_advisor
from chronos.application_errors_and_permissions import WrongRoleError


def test_list_clients_requires_advisor_role(db, alice):
    with pytest.raises(WrongRoleError):
        list_clients_for_advisor(db, alice.id)


def test_list_clients_returns_investors(db, advisor):
    clients = list_clients_for_advisor(db, advisor.id)
    assert len(clients) == 1
    assert clients[0].client_email == "alice@example.com"
    assert all(client.total_value == pytest.approx(100_000.0) for client in clients)


def test_advisor_cannot_trade_for_clients(client, advisor):
    response = client.post(
        "/trades",
        json={"user_id": advisor.id, "symbol": "AAPL", "side": "BUY", "amount": 1000.0},
    )
    assert response.status_code == 403
