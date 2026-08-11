"""Testes das rotas de chat (/chat)

`answer_question` é substituída por uma função fake nos testes que exercitam
o envio de mensagens — os testes de rota não devem depender da API da
Claude estar configurada nem gastar créditos de verdade.
"""
from app.routes import chat as chat_routes
from app.services import document_service


def _auth_headers(client):
    client.post(
        "/auth/register",
        json={"username": "joao", "email": "joao@example.com", "password": "senha123"},
    )
    token = client.post(
        "/auth/login", json={"username": "joao", "password": "senha123"}
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _fake_embed_texts(texts):
    return [[0.1, 0.2, 0.3] for _ in texts]


def _upload_ready_document(client, headers, monkeypatch):
    monkeypatch.setattr(document_service, "embed_texts", _fake_embed_texts)
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "manual.txt",
                b"O produto X deve ser usado apenas em ambientes internos.",
                "text/plain",
            )
        },
        headers=headers,
    )
    return response.json()


def test_create_session_requires_ready_document(client, monkeypatch):
    headers = _auth_headers(client)
    doc = _upload_ready_document(client, headers, monkeypatch)

    response = client.post("/chat/sessions", json={"document_id": doc["id"]}, headers=headers)

    assert response.status_code == 201
    assert response.json()["document_id"] == doc["id"]


def test_send_message_returns_assistant_answer(client, monkeypatch):
    headers = _auth_headers(client)
    doc = _upload_ready_document(client, headers, monkeypatch)
    session = client.post(
        "/chat/sessions", json={"document_id": doc["id"]}, headers=headers
    ).json()

    def _fake_answer_question(db, document_id, question, history):
        return "O produto X deve ser usado apenas em ambientes internos.", 1

    monkeypatch.setattr(chat_routes, "answer_question", _fake_answer_question)

    response = client.post(
        f"/chat/sessions/{session['id']}/messages",
        json={"content": "Onde o produto X pode ser usado?"},
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "assistant"
    assert "ambientes internos" in data["content"]

    history = client.get(f"/chat/sessions/{session['id']}/messages", headers=headers).json()
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


def test_send_message_surfaces_api_errors_as_502(client, monkeypatch):
    headers = _auth_headers(client)
    doc = _upload_ready_document(client, headers, monkeypatch)
    session = client.post(
        "/chat/sessions", json={"document_id": doc["id"]}, headers=headers
    ).json()

    def _broken_answer_question(db, document_id, question, history):
        raise RuntimeError("Claude API indisponível")

    monkeypatch.setattr(chat_routes, "answer_question", _broken_answer_question)

    response = client.post(
        f"/chat/sessions/{session['id']}/messages",
        json={"content": "Alguma pergunta"},
        headers=headers,
    )

    assert response.status_code == 502


def test_chat_requires_authentication(client):
    response = client.get("/chat/sessions")
    assert response.status_code == 401
