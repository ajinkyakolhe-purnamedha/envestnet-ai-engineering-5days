"""The advisor assistant endpoint, as shipped.

The endpoint serves the participant-built workflow from
labs/m8_advisor_assistant. These tests stay green before AND after the
M8 lab: role checks always apply, and the assistant answers either 501
(stubs not yet implemented) or 200 (lab complete). The full behavioral
tests live with the lab: labs/m8_advisor_assistant/test_m8_lab.py.
"""


def test_investor_cannot_use_the_assistant(client, db, alice):
    response = client.post(
        f"/advisor/clients/{alice.id}/assistant",
        params={"advisor_user_id": alice.id},
        json={"question": "How is the portfolio?"},
    )
    assert response.status_code == 403


def test_assistant_answers_or_reports_unfinished_lab(client, db, alice, advisor):
    response = client.post(
        f"/advisor/clients/{alice.id}/assistant",
        params={"advisor_user_id": advisor.id},
        json={"question": "How is this portfolio positioned?"},
    )
    assert response.status_code in (200, 501)
    if response.status_code == 501:
        assert "M8" in response.json()["detail"]
