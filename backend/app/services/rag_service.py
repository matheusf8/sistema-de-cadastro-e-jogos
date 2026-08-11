"""
Serviço de RAG (Retrieval-Augmented Generation).

Busca os trechos mais relevantes de um documento para uma pergunta (por
similaridade de cosseno, calculada "na unha" com numpy — não há banco
vetorial dedicado, o volume de um projeto de portfólio não justifica) e
usa a API da Claude para gerar a resposta com base apenas nesses trechos.
"""
from typing import List, Tuple

import numpy as np
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import DocumentChunk
from app.services.embedding_service import cosine_similarity, deserialize_embedding, embed_text


def retrieve_relevant_chunks(
    db: Session, document_id: int, question: str, top_k: int
) -> List[DocumentChunk]:
    """Retorna os `top_k` chunks do documento mais similares à pergunta."""
    chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).all()
    if not chunks:
        return []

    query_vector = np.array(embed_text(question), dtype=np.float32)

    scored = [
        (cosine_similarity(query_vector, deserialize_embedding(chunk.embedding)), chunk)
        for chunk in chunks
    ]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]


def build_system_prompt(context_chunks: List[DocumentChunk]) -> str:
    """Monta o system prompt com os trechos recuperados como contexto."""
    context = "\n\n---\n\n".join(
        f"[Trecho {i + 1}]\n{chunk.content}" for i, chunk in enumerate(context_chunks)
    )
    return (
        "Você é um assistente que responde perguntas com base apenas no "
        "conteúdo de um documento fornecido pelo usuário. Use somente as "
        "informações dos trechos abaixo para responder. Se a resposta não "
        "estiver nos trechos, diga claramente que não encontrou essa "
        "informação no documento — não invente.\n\n"
        f"Trechos do documento:\n\n{context}"
    )


def answer_question(
    db: Session, document_id: int, question: str, history: list
) -> Tuple[str, int]:
    """
    Responde a uma pergunta sobre um documento usando RAG.

    `history` é a lista de mensagens anteriores da sessão (sem a pergunta
    atual), no formato esperado pela API da Claude: [{"role", "content"}].

    Retorna a resposta em texto e o número de trechos usados como contexto.
    """
    import anthropic

    relevant_chunks = retrieve_relevant_chunks(db, document_id, question, settings.TOP_K_CHUNKS)

    if not relevant_chunks:
        return (
            "Ainda não há conteúdo indexado para este documento. Tente reenviá-lo.",
            0,
        )

    if not settings.ANTHROPIC_API_KEY:
        raise RuntimeError(
            "ANTHROPIC_API_KEY não configurada no backend (.env). "
            "Defina sua chave em https://console.anthropic.com/settings/keys."
        )

    system_prompt = build_system_prompt(relevant_chunks)
    # Timeout curto proposital: numa requisição síncrona de chat, é melhor
    # falhar rápido (e o frontend mostrar o erro) do que travar a interface
    # esperando o timeout padrão do SDK (10 minutos).
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY, timeout=30.0, max_retries=1)

    response = client.messages.create(
        model=settings.CLAUDE_MODEL,
        max_tokens=1024,
        system=system_prompt,
        messages=history + [{"role": "user", "content": question}],
    )

    answer = next((block.text for block in response.content if block.type == "text"), "")
    return answer, len(relevant_chunks)
