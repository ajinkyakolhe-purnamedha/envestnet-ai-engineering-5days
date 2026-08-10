"""Demo login works; wrong roles are rejected server-side."""

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
    emails = {user["email"] for user in response.json()}
    assert {ALICE_EMAIL, ADVISOR_EMAIL} <= emails


def test_advisor_rejected_from_investor_portfolio(client, advisor):
    response = client.get("/portfolio", params={"user_id": advisor.id})
    assert response.status_code == 403


def test_investor_rejected_from_advisor_clients(client, alice):
    response = client.get("/advisor/clients", params={"advisor_user_id": alice.id})
    assert response.status_code == 403
