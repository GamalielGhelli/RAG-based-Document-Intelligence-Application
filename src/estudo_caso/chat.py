import ollama

MODELO = "gemma3:1b"

MAX_CARACTERES_DOCUMENTO = 30000


def perguntar_documento(
    texto_documento: str,
    pergunta: str,
    historico: list[dict] | None = None,
) -> str:
    """
    Faz uma pergunta ao LLM utilizando
    o conteúdo do documento como contexto.
    """

    contexto = texto_documento[
        :MAX_CARACTERES_DOCUMENTO
    ]

    prompt_sistema = f"""
Você é um assistente especializado em consulta de documentos.

Responda utilizando apenas as informações presentes
no documento fornecido abaixo.

Se a informação não estiver presente no documento,
informe que não foi possível encontrá-la.

Se o usuário pedir um resumo, produza um resumo objetivo
dos principais pontos do documento.

DOCUMENTO:

{contexto}
"""

    mensagens = [
        {
            "role": "system",
            "content": prompt_sistema,
        }
    ]

    if historico:
        mensagens.extend(
            historico[-6:]
        )

    mensagens.append(
        {
            "role": "user",
            "content": pergunta,
        }
    )

    resposta = ollama.chat(
        model=MODELO,
        messages=mensagens,
        options={
            "temperature": 0.2,
        },
    )

    return resposta[
        "message"
    ]["content"]