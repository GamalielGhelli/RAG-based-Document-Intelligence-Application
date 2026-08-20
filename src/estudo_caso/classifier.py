import ollama

MODEL = "gemma3:1b"


def classify_document(text: str) -> str:
    """
    Classifica o documento como:
    Lei, Portaria, Resolução ou Outro.
    """

    sample = text[:5000]

    prompt = f"""
Classifique o documento abaixo em apenas uma das categorias:

Lei
Portaria
Resolução
Outro

Responda SOMENTE com o nome da categoria.

Não explique a resposta.

Documento:

{sample}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        options={
            "temperature": 0,
        },
    )

    result = response["message"]["content"].strip()

    if "Lei" in result:
        return "Lei"

    if "Portaria" in result:
        return "Portaria"

    if "Resolução" in result or "Resolucao" in result:
        return "Resolução"

    return "Outro"