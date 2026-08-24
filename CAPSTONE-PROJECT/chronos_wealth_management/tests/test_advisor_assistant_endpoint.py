"""The shipped advisor assistant endpoint always has a runtime fallback."""


def test_investor_cannot_use_the_assistant(client, db, alice):
    response = client.post(
        f"/advisor/clients/{alice.id}/assistant",
        params={"advisor_user_id": alice.id},
        json={"question": "How is the portfolio?"},
    )
    assert response.status_code == 403


def test_assistant_answers_without_an_unfinished_lab_response(client, db, alice, advisor):
    response = client.post(
        f"/advisor/clients/{alice.id}/assistant",
        params={"advisor_user_id": advisor.id},
        json={"question": "How is this portfolio positioned?"},
    )
    assert response.status_code == 200
