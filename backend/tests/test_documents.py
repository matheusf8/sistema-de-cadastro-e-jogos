"""Testes das rotas de documentos (/documents)

Os testes substituem `embed_texts` por uma função fake (vetores fixos) para
não depender do download do modelo de embeddings real durante a suíte.
"""
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


def test_upload_document_processes_and_indexes(client, monkeypatch):
    monkeypatch.setattr(document_service, "embed_texts", _fake_embed_texts)
    headers = _auth_headers(client)

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "relatorio.txt",
                b"Este e um documento de teste com conteudo relevante.",
                "text/plain",
            )
        },
        headers=headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "relatorio.txt"
    assert data["status"] == "ready"
    assert data["chunk_count"] == 1


def test_upload_rejects_unsupported_format(client):
    headers = _auth_headers(client)

    response = client.post(
        "/documents/upload",
        files={"file": ("imagem.png", b"binario", "image/png")},
        headers=headers,
    )

    assert response.status_code == 400


def test_list_documents_returns_only_own_documents(client, monkeypatch):
    monkeypatch.setattr(document_service, "embed_texts", _fake_embed_texts)
    headers = _auth_headers(client)
    client.post(
        "/documents/upload",
        files={"file": ("a.txt", b"conteudo a", "text/plain")},
        headers=headers,
    )

    response = client.get("/documents/", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_document(client, monkeypatch):
    monkeypatch.setattr(document_service, "embed_texts", _fake_embed_texts)
    headers = _auth_headers(client)
    doc = client.post(
        "/documents/upload",
        files={"file": ("a.txt", b"conteudo a", "text/plain")},
        headers=headers,
    ).json()

    response = client.delete(f"/documents/{doc['id']}", headers=headers)
    assert response.status_code == 204

    response = client.get("/documents/", headers=headers)
    assert response.json() == []


def test_documents_require_authentication(client):
    response = client.get("/documents/")
    assert response.status_code == 401
