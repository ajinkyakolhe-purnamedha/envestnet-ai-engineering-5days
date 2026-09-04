"""End-to-end API behavior through the FastAPI test client."""

import pytest


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_assets_lists_five_symbols(client):
    symbols = [asset["symbol"] for asset in client.get("/assets").json()]
    assert symbols == ["AAPL", "GLD", "JPM", "MSFT", "SPY"]


def test_account_endpoint(client, alice):
    response = client.get("/account", params={"user_id": alice.id})
    assert response.status_code == 200
    account = response.json()
    assert account["cash_balance"] == 100_000.0
    assert account["simulated_date"] == "2020-06-01"


def test_unknown_user_is_404(client):
    assert client.get("/account", params={"user_id": 999}).status_code == 404


def test_market_history_endpoint_hides_future(client, alice):
    response = client.get(
        f"/market/AAPL/history", params={"user_id": alice.id, "trading_days": 60}
    )
    assert response.status_code == 200
    history = response.json()
    assert history
    assert max(point["date"] for point in history) <= "2020-06-01"


def test_market_history_unknown_symbol_is_404(client, alice):
    response = client.get("/market/ZZZZ/history", params={"user_id": alice.id})
    assert response.status_code == 404


def test_symbol_without_prices_is_400_on_trade(client, alice):
    response = client.post(
        "/trades",
        json={"user_id": alice.id, "symbol": "SPY", "side": "BUY", "amount": 1000.0},
    )
    assert response.status_code == 400


def test_trade_preview_execute_and_portfolio_flow(client, alice):
    preview = client.post(
        "/trades/preview",
        json={"user_id": alice.id, "symbol": "AAPL", "side": "BUY", "amount": 10800.0},
    ).json()
    assert preview["valid"] is True
    assert preview["price"] == 108.0
    assert preview["shares"] == pytest.approx(100.0)

    executed = client.post(
        "/trades",
        json={"user_id": alice.id, "symbol": "AAPL", "side": "BUY", "amount": 10800.0},
    )
    assert executed.status_code == 200

    portfolio = client.get("/portfolio", params={"user_id": alice.id}).json()
    assert portfolio["cash_balance"] == pytest.approx(89_200.0)
    assert portfolio["holdings"][0]["symbol"] == "AAPL"

    trades = client.get("/trades", params={"user_id": alice.id}).json()
    assert len(trades) == 1

    history = client.get(
        "/portfolio/account-value-history", params={"user_id": alice.id}
    ).json()
    assert history


def test_insufficient_cash_is_400(client, alice):
    response = client.post(
        "/trades",
        json={"user_id": alice.id, "symbol": "AAPL", "side": "BUY", "amount": 500000.0},
    )
    assert response.status_code == 400


def test_invalid_side_is_422(client, alice):
    response = client.post(
        "/trades",
        json={"user_id": alice.id, "symbol": "AAPL", "side": "HOLD", "amount": 100.0},
    )
    assert response.status_code == 422


def test_advisor_client_portfolio_flow(client, alice, advisor):
    clients = client.get(
        "/advisor/clients", params={"advisor_user_id": advisor.id}
    ).json()
    assert len(clients) == 1
    assert clients[0]["client_user_id"] == alice.id

    portfolio = client.get(
        f"/advisor/clients/{alice.id}/portfolio",
        params={"advisor_user_id": advisor.id},
    )
    assert portfolio.status_code == 200


def test_demo_reset_restores_starting_state(client, alice):
    client.post(
        "/trades",
        json={"user_id": alice.id, "symbol": "AAPL", "side": "BUY", "amount": 10800.0},
    )
    reset = client.post("/demo/reset")
    assert reset.status_code == 200
    assert reset.json()["accounts_reset"] == 1

    portfolio = client.get("/portfolio", params={"user_id": alice.id}).json()
    assert portfolio["cash_balance"] == 100_000.0
    assert portfolio["holdings"] == []


def test_history_endpoint_respects_trading_days(client, alice):
    response = client.get(
        "/market/AAPL/history", params={"user_id": alice.id, "trading_days": 2}
    )
    assert len(response.json()) == 2


def test_invalid_advance_step_is_422(client, alice):
    response = client.post(
        "/simulation/advance", json={"user_id": alice.id, "step": "2W"}
    )
    assert response.status_code == 422
