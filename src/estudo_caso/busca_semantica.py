import numpy as np
import ollama

EMBEDDING_MODEL = "embeddinggemma"


def criar_embedding(texto: str) -> np.ndarray:
    """
    Converte um texto em um vetor numérico (embedding).
    """

    if not texto or not texto.strip():
        raise ValueError(
            "Não é possível gerar embedding de um texto vazio."
        )

    amostra = texto[:8000]

    resposta = ollama.embed(
        model=EMBEDDING_MODEL,
        input=amostra,
    )

    embeddings = resposta["embeddings"]

    if len(embeddings) == 0:
        raise ValueError(
            "O Ollama não retornou nenhum embedding."
        )

    return np.array(
        embeddings[0],
        dtype=np.float32,
    )


def similaridade_cosseno(
    vetor_a: np.ndarray,
    vetor_b: np.ndarray,
) -> float:

    numerador = np.dot(
        vetor_a,
        vetor_b,
    )

    denominador = (
        np.linalg.norm(vetor_a)
        * np.linalg.norm(vetor_b)
    )

    if denominador == 0:
        return 0.0

    return float(
        numerador / denominador
    )


def buscar_documentos(
    consulta: str,
    documentos: list[dict],
    quantidade_resultados: int = 3,
) -> list[dict]:

    embedding_consulta = criar_embedding(
        consulta
    )

    resultados = []

    for documento in documentos:

        if documento["embedding"] is None:
            continue

        similaridade = similaridade_cosseno(
            embedding_consulta,
            documento["embedding"],
        )

        resultados.append(
            {
                "nome": documento["nome"],
                "tipo": documento["tipo"],
                "similaridade": similaridade,
            }
        )

    resultados.sort(
        key=lambda item: item["similaridade"],
        reverse=True,
    )

    return resultados[:quantidade_resultados]