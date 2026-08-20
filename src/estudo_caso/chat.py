import ollama

MODEL = "gemma3:1b"

MAX_DOCUMENT_CHARS = 30000

def ask_document(
    document_text: str,
    question: str,
    history: list[dict] | None = None,
) -> str:
    """
    Faz uma pergunta ao LLM utilizando
    o conteúdo do documento como contexto.
    """
    context = document_text[:MAX_DOCUMENT_CHARS]
    system_prompt = f"""
Você é um assistente especializado em consulta de documentos.

Responda utilizando apenas as informações presentes
no documento fornecido abaixo.

Se a informação não estiver presente no documento,
informe que não foi possível encontrá-la.

Se o usuário pedir um resumo, produza um resumo objetivo
dos principais pontos do documento.

DOCUMENTO:

{context}
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    if history:
        messages.extend(history[-6:])

    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    response = ollama.chat(
        model=MODEL,
        messages=messages,
        options={
            "temperature": 0.2,
        },
    )

    return response["message"]["content"]