"""
Serviço de embeddings locais (sentence-transformers)

Gera embeddings de texto sem depender de nenhuma API externa — o modelo
roda localmente, o que evita custo e uma segunda chave de API. O modelo é
carregado uma única vez (lru_cache) e reaproveitado entre as chamadas.
"""
import json
from functools import lru_cache
from typing import List

import numpy as np

from app.core.config import settings


@lru_cache(maxsize=1)
def _get_model():
    # Import tardio: evita carregar o modelo (e o torch, que é pesado) só
    # por importar este módulo — por exemplo em testes que mockam embeddings
    # e nunca chegam a chamar o modelo de verdade.
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(settings.EMBEDDING_MODEL)


def embed_text(text: str) -> List[float]:
    """Gera o vetor de embedding de um único texto."""
    model = _get_model()
    vector = model.encode(text, normalize_embeddings=True)
    return vector.tolist()


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Gera embeddings para uma lista de textos de uma vez (mais eficiente)."""
    if not texts:
        return []
    model = _get_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return vectors.tolist()


def serialize_embedding(vector: List[float]) -> str:
    """Serializa um vetor para salvar numa coluna de texto do banco."""
    return json.dumps(vector)


def deserialize_embedding(raw: str) -> np.ndarray:
    """Desserializa um vetor salvo no banco de volta para numpy array."""
    return np.array(json.loads(raw), dtype=np.float32)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Similaridade de cosseno entre dois vetores."""
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)
