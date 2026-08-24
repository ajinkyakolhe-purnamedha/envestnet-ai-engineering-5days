"""Demo login works; wrong roles are rejected server-side."""

from datetime import date

from chronos.shared_database.database_tables import Account, User
from tests.conftest import ADVISOR_EMAIL, ALICE_EMAIL


def test_login_demo_investor(client):
    response = client.post("/auth/login", json={"email": ALICE_EMAIL})
    assert response.status_code == 200
    assert response.json()["role"] == "INVESTOR"


def test_login_normalizes_email(client):
    response = client.post("/auth/login", json={"email": "  Alice@Example.com  "})
    assert response.status_code == 200
    assert response.json()["email"] == ALICE_EMAIL


def test_login_unknown_email_fails(client):
    response = client.post("/auth/login", json={"email": "nobody@example.com"})
    assert response.status_code == 404


def test_demo_users_listed(client):
    response = client.get("/auth/demo-users")
    assert response.status_code == 200
    assert [
        (user["email"], user["name"], user["role"])
        for user in response.json()
    ] == [
        (ALICE_EMAIL, "Alice Investor", "INVESTOR"),
        (ADVISOR_EMAIL, "Demo Advisor", "ADVISOR"),
    ]


def test_reset_removes_legacy_bob_demo_data(client, db):
    bob = User(
        email="bob@example.com", name="Bob Investor", role="INVESTOR"
    )
    db.add(bob)
    db.flush()
    db.add(
        Account(
            user_id=bob.id,
            name="Bob Investor Account",
            cash_balance=100_000.0,
            initial_cash=100_000.0,
            simulated_date=date(2020, 6, 1),
        )
    )
    db.flush()

    response = client.post("/demo/reset")

    assert response.status_code == 200
    assert db.query(User).filter(User.email == "bob@example.com").one_or_none() is None
    assert response.json()["accounts_reset"] == 1


def test_advisor_rejected_from_investor_portfolio(client, advisor):
    response = client.get("/portfolio", params={"user_id": advisor.id})
    assert response.status_code == 403


def test_investor_rejected_from_advisor_clients(client, alice):
    response = client.get("/advisor/clients", params={"advisor_user_id": alice.id})
    assert response.status_code == 403
