"""One core investor-to-advisor journey through the HTTP API."""

import pytest

from tests.conftest import ADVISOR_EMAIL, ALICE_EMAIL

BUY_AMOUNT = 10_800.0  # exactly 100 AAPL shares at the 2020-06-01 close of 108


def test_end_to_end_investor_and_advisor_workflow(client):
    alice = client.post("/auth/login", json={"email": ALICE_EMAIL}).json()
    alice_id = alice["id"]
    portfolio = client.get("/portfolio", params={"user_id": alice_id}).json()
    assert portfolio["holdings"] == []
    assert portfolio["total_value"] == 100_000.0

    preview = client.post(
        "/trades/preview",
        json={"user_id": alice_id, "symbol": "AAPL", "side": "BUY", "amount": BUY_AMOUNT},
    ).json()
    assert preview["valid"] is True
    assert preview["price"] == 108.0
    assert preview["shares"] == pytest.approx(100.0)

    assert client.post(
        "/trades",
        json={"user_id": alice_id, "symbol": "AAPL", "side": "BUY", "amount": BUY_AMOUNT},
    ).status_code == 200

    advance = client.post(
        "/simulation/advance", json={"user_id": alice_id, "step": "1M"}
    ).json()
    assert advance["previous_portfolio"]["simulated_date"] == "2020-06-01"
    assert advance["account"]["simulated_date"] == "2020-07-01"
    assert advance["portfolio"]["simulated_date"] == "2020-07-01"
    assert advance["portfolio"]["holdings_value"] == pytest.approx(11_600.0)
    advanced_date = advance["account"]["simulated_date"]

    value_history = client.get(
        "/portfolio/account-value-history", params={"user_id": alice_id}
    ).json()
    assert value_history
    assert max(point["date"] for point in value_history) <= advanced_date

    advisor = client.post("/auth/login", json={"email": ADVISOR_EMAIL}).json()
    advisor_id = advisor["id"]
    advisor_view = client.get(
        f"/advisor/clients/{alice_id}/portfolio",
        params={"advisor_user_id": advisor_id},
    ).json()
    assert advisor_view["simulated_date"] == advanced_date
    assert advisor_view["holdings"][0]["symbol"] == "AAPL"

    assert client.post(
        "/trades",
        json={"user_id": advisor_id, "symbol": "AAPL", "side": "BUY", "amount": 100.0},
    ).status_code == 403
