"""Testes do CRUD de notas (/notes) — todas as rotas exigem autenticação"""


def _register_and_login(client, username="maria"):
    client.post(
        "/auth/register",
        json={"username": username, "email": f"{username}@example.com", "password": "senha123"},
    )
    token = client.post(
        "/auth/login", json={"username": username, "password": "senha123"}
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_notes_require_authentication(client):
    response = client.get("/notes/")

    assert response.status_code == 401


def test_create_and_list_notes(client):
    headers = _register_and_login(client)

    created = client.post(
        "/notes/", json={"title": "Primeira nota", "content": "conteúdo"}, headers=headers
    )
    assert created.status_code == 201
    assert created.json()["title"] == "Primeira nota"

    listed = client.get("/notes/", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_update_note(client):
    headers = _register_and_login(client)
    note_id = client.post("/notes/", json={"title": "Original"}, headers=headers).json()["id"]

    response = client.put(
        f"/notes/{note_id}", json={"title": "Editada"}, headers=headers
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Editada"


def test_delete_note(client):
    headers = _register_and_login(client)
    note_id = client.post("/notes/", json={"title": "Para deletar"}, headers=headers).json()["id"]

    deleted = client.delete(f"/notes/{note_id}", headers=headers)
    assert deleted.status_code == 204

    missing = client.get(f"/notes/{note_id}", headers=headers)
    assert missing.status_code == 404


def test_note_not_found_returns_404(client):
    headers = _register_and_login(client)

    response = client.get("/notes/999", headers=headers)

    assert response.status_code == 404


def test_notes_are_isolated_per_user(client):
    headers_maria = _register_and_login(client, "maria")
    client.post("/notes/", json={"title": "Nota da Maria"}, headers=headers_maria)

    headers_joao = _register_and_login(client, "joao")
    response = client.get("/notes/", headers=headers_joao)

    assert response.status_code == 200
    assert response.json() == []
