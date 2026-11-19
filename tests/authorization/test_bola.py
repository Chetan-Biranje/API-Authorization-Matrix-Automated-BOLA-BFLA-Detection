from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_user_can_access_own_object():
    response = client.get(
        "/users/1",
        headers={"Authorization": "Bearer user-token"},
    )

    assert response.status_code == 200
    assert response.json()["user"]["id"] == 1


def test_user_cannot_access_another_users_object():
    response = client.get(
        "/users/2",
        headers={"Authorization": "Bearer user-token"},
    )

    # Passes on the default (secure) app; fails when LAB_VULNERABLE=1.
    assert response.status_code == 403
