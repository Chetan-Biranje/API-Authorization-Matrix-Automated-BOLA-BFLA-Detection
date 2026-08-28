from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_normal_user_cannot_access_admin_function():
    response = client.get(
        "/admin/users",
        headers={"Authorization": "Bearer user-token"},
    )

    assert response.status_code == 403


def test_manager_cannot_access_admin_function():
    response = client.get(
        "/admin/users",
        headers={"Authorization": "Bearer manager-token"},
    )

    assert response.status_code == 403


def test_admin_can_access_admin_function():
    response = client.get(
        "/admin/users",
        headers={"Authorization": "Bearer admin-token"},
    )

    assert response.status_code == 200
