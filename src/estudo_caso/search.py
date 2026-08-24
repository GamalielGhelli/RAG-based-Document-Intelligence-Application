import numpy as np
import ollama

EMBEDDING_MODEL = "embeddinggemma"


def create_embedding(text: str) -> np.ndarray:
    """
    Converte um texto em um vetor numérico (embedding).
    """

    if not text or not text.strip():
        raise ValueError(
            "Não é possível gerar embedding de um texto vazio."
        )

    sample = text[:8000]

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=sample,
    )

    embeddings = response["embeddings"]

    if len(embeddings) == 0:
        raise ValueError(
            "O Ollama não retornou nenhum embedding."
        )

    return np.array(
        embeddings[0],
        dtype=np.float32,
    )


def cosine_similarity(
    vector_a: np.ndarray,
    vector_b: np.ndarray,
) -> float:

    numerator = np.dot( 
        vector_a,
        vector_b,
    )

    denominator = (
        np.linalg.norm(vector_a)
        * np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return 0.0
    
    return float(
        numerator / denominator
    )


def search_documents(
    query: str,
    documents: list[dict],
    top_k: int = 3,
) -> list[dict]:

    query_embedding = create_embedding(query)

    results = []

    for document in documents:

        if document["embedding"] is None:
            continue

        score = cosine_similarity(
            query_embedding,
            document["embedding"],
        )

        results.append(
            {
                "name": document["name"],
                "type": document["type"],
                "score": score,
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]