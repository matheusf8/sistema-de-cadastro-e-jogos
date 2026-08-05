"""Testes das rotas de autenticação (/auth)"""


def test_register_creates_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "joao",
            "email": "joao@example.com",
            "password": "senha123",
            "full_name": "João Silva",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "joao"
    assert data["email"] == "joao@example.com"
    assert "hashed_password" not in data
    assert "password" not in data


def test_register_rejects_duplicate_username_or_email(client):
    payload = {"username": "joao", "email": "joao@example.com", "password": "senha123"}
    client.post("/auth/register", json=payload)

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 400


def test_register_rejects_short_password(client):
    response = client.post(
        "/auth/register",
        json={"username": "joao", "email": "joao@example.com", "password": "123"},
    )

    assert response.status_code == 422


def test_login_returns_token(client):
    client.post(
        "/auth/register",
        json={"username": "joao", "email": "joao@example.com", "password": "senha123"},
    )

    response = client.post("/auth/login", json={"username": "joao", "password": "senha123"})

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert data["user"]["username"] == "joao"


def test_login_rejects_wrong_password(client):
    client.post(
        "/auth/register",
        json={"username": "joao", "email": "joao@example.com", "password": "senha123"},
    )

    response = client.post("/auth/login", json={"username": "joao", "password": "errada"})

    assert response.status_code == 401


def test_login_rejects_unknown_user(client):
    response = client.post("/auth/login", json={"username": "ninguem", "password": "senha123"})

    assert response.status_code == 401


def test_me_requires_authentication(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_me_returns_current_user(client):
    client.post(
        "/auth/register",
        json={"username": "joao", "email": "joao@example.com", "password": "senha123"},
    )
    token = client.post(
        "/auth/login", json={"username": "joao", "password": "senha123"}
    ).json()["access_token"]

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["username"] == "joao"
