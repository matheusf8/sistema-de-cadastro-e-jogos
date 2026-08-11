"""Testes unitários do serviço de RAG, sem chamar a API da Claude de verdade.

Achado durante teste manual: sem `ANTHROPIC_API_KEY` configurada, a chamada
ficava pendurada até o timeout padrão do SDK (10 minutos) em vez de falhar
rápido — travando a interface. Esses testes travam a correção (falha
imediata com mensagem clara) para não regredir.
"""
from app.core.config import settings
from app.services import rag_service


class _FakeChunk:
    def __init__(self, content):
        self.content = content


def test_answer_question_fails_fast_without_api_key(monkeypatch):
    monkeypatch.setattr(settings, "ANTHROPIC_API_KEY", "")
    monkeypatch.setattr(
        rag_service,
        "retrieve_relevant_chunks",
        lambda db, document_id, question, top_k: [_FakeChunk("algum trecho")],
    )

    try:
        rag_service.answer_question(db=None, document_id=1, question="oi", history=[])
        assert False, "deveria ter levantado RuntimeError"
    except RuntimeError as exc:
        assert "ANTHROPIC_API_KEY" in str(exc)


def test_answer_question_returns_fallback_when_no_chunks_indexed(monkeypatch):
    monkeypatch.setattr(settings, "ANTHROPIC_API_KEY", "sk-ant-fake-para-teste")
    monkeypatch.setattr(
        rag_service, "retrieve_relevant_chunks", lambda db, document_id, question, top_k: []
    )

    answer, chunks_used = rag_service.answer_question(db=None, document_id=1, question="oi", history=[])

    assert chunks_used == 0
    assert "reenviá-lo" in answer
