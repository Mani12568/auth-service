from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_signup_success():
    response = client.post("/signup", params={"email": "pytest_user1@example.com", "password": "testpass123"})
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data


def test_signup_duplicate_email():
    client.post("/signup", params={"email": "duplicate@example.com", "password": "testpass123"})
    response = client.post("/signup", params={"email": "duplicate@example.com", "password": "testpass123"})
    assert response.status_code == 400


def test_login_wrong_password():
    client.post("/signup", params={"email": "wrongpass@example.com", "password": "correctpass"})
    response = client.post("/login", params={"email": "wrongpass@example.com", "password": "wrongpass"})
    assert response.status_code == 401


def test_login_success_and_protected_route():
    client.post("/signup", params={"email": "fulltest@example.com", "password": "testpass123"})
    login_response = client.post("/login", params={"email": "fulltest@example.com", "password": "testpass123"})
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    me_response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "fulltest@example.com"


def test_protected_route_without_token():
    response = client.get("/me")
    assert response.status_code == 401