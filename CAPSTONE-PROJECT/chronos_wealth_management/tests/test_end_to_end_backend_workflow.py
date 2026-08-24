"""Full investor and advisor journey through HTTP, in one continuous story.

Runs against the FastAPI app via TestClient with fixture prices loaded into a
temporary SQLite database (see conftest). No Chrome, no Streamlit, no network.

Fixture prices at the starting simulated date 2020-06-01: AAPL closes 108 and
rises 2 per week; the fixture ends 2020-09-14.
"""

import pytest

from tests.conftest import ADVISOR_EMAIL, ALICE_EMAIL

BUY_AMOUNT = 10_800.0  # exactly 100 AAPL shares at the 2020-06-01 close of 108


def test_end_to_end_investor_and_advisor_workflow(client):
    # 1. health
    assert client.get("/health").json() == {"status": "ok"}

    # 2. demo users
    demo_users = client.get("/auth/demo-users").json()
    assert {user["email"] for user in demo_users} >= {ALICE_EMAIL, ADVISOR_EMAIL}

    # 3. login as Alice
    alice = client.post("/auth/login", json={"email": ALICE_EMAIL}).json()
    assert alice["role"] == "INVESTOR"
    alice_id = alice["id"]

    # 4. Alice's account
    account = client.get("/account", params={"user_id": alice_id}).json()
    assert account["cash_balance"] == 100_000.0
    simulated_date = account["simulated_date"]
    assert simulated_date == "2020-06-01"

    # 5. Alice's starting portfolio
    portfolio = client.get("/portfolio", params={"user_id": alice_id}).json()
    assert portfolio["holdings"] == []
    assert portfolio["total_value"] == 100_000.0

    # 6. AAPL chart data — never past the simulated date
    history = client.get(
        "/market/AAPL/history", params={"user_id": alice_id}
    ).json()
    assert history
    assert max(point["date"] for point in history) <= simulated_date

    # 7. preview an AAPL buy — valid shares and price
    preview = client.post(
        "/trades/preview",
        json={"user_id": alice_id, "symbol": "AAPL", "side": "BUY", "amount": BUY_AMOUNT},
    ).json()
    assert preview["valid"] is True
    assert preview["price"] == 108.0
    assert preview["shares"] == pytest.approx(100.0)

    # 8. execute the buy — creates a trade
    trade = client.post(
        "/trades",
        json={"user_id": alice_id, "symbol": "AAPL", "side": "BUY", "amount": BUY_AMOUNT},
    )
    assert trade.status_code == 200
    assert trade.json()["simulated_date"] == simulated_date

    # 9. portfolio now shows the AAPL holding and lower cash
    portfolio = client.get("/portfolio", params={"user_id": alice_id}).json()
    assert portfolio["cash_balance"] == pytest.approx(100_000.0 - BUY_AMOUNT)
    assert [holding["symbol"] for holding in portfolio["holdings"]] == ["AAPL"]
    assert portfolio["holdings"][0]["shares"] == pytest.approx(100.0)
    # valuation still uses the simulated-date price, not anything later
    assert portfolio["holdings"][0]["current_price"] == 108.0

    # 10. trade history
    trades = client.get("/trades", params={"user_id": alice_id}).json()
    assert len(trades) == 1
    assert trades[0]["side"] == "BUY"

    # 11-12. advance one month — before/after snapshots, new simulated date
    advance = client.post(
        "/simulation/advance", json={"user_id": alice_id, "step": "1M"}
    ).json()
    assert advance["previous_portfolio"]["simulated_date"] == "2020-06-01"
    assert advance["account"]["simulated_date"] == "2020-07-01"
    assert advance["portfolio"]["simulated_date"] == "2020-07-01"
    # AAPL close on the latest fixture date <= 2020-07-01 (2020-06-29) is 116
    assert advance["portfolio"]["holdings_value"] == pytest.approx(11_600.0)
    advanced_date = advance["account"]["simulated_date"]

    # 13. account value history reaches the current simulated date, no further
    value_history = client.get(
        "/portfolio/account-value-history", params={"user_id": alice_id}
    ).json()
    assert value_history
    assert max(point["date"] for point in value_history) <= advanced_date
    assert value_history[-1]["total_value"] == pytest.approx(89_200.0 + 11_600.0)

    # 14. login as the advisor
    advisor = client.post("/auth/login", json={"email": ADVISOR_EMAIL}).json()
    assert advisor["role"] == "ADVISOR"
    advisor_id = advisor["id"]

    # 15. advisor sees the supported investor client
    clients = client.get(
        "/advisor/clients", params={"advisor_user_id": advisor_id}
    ).json()
    assert {row["client_user_id"] for row in clients} == {alice_id}

    # 16. advisor reads Alice's portfolio through the advisor route
    advisor_view = client.get(
        f"/advisor/clients/{alice_id}/portfolio",
        params={"advisor_user_id": advisor_id},
    ).json()
    assert advisor_view["simulated_date"] == advanced_date
    assert advisor_view["holdings"][0]["symbol"] == "AAPL"

    # 17. advisor report uses Alice's simulated date, with metrics and advice
    report = client.post(
        f"/advisor/clients/{alice_id}/report",
        params={"advisor_user_id": advisor_id},
    ).json()
    assert report["simulated_date"] == advanced_date
    assert report["metrics"]["number_of_holdings"] == 1
    assert report["recommendations"]  # high cash + low diversification here

    # 18. advisor cannot execute trades
    advisor_trade = client.post(
        "/trades",
        json={"user_id": advisor_id, "symbol": "AAPL", "side": "BUY", "amount": 100.0},
    )
    assert advisor_trade.status_code == 403

    # 19. investor cannot call advisor routes
    investor_as_advisor = client.get(
        "/advisor/clients", params={"advisor_user_id": alice_id}
    )
    assert investor_as_advisor.status_code == 403
