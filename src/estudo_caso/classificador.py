import re
import unicodedata


def normalizar_texto(texto: str) -> str:
    """
    Normaliza o texto para facilitar comparações.

    - transforma em minúsculas
    - remove acentos
    """

    texto = texto.casefold()

    texto = unicodedata.normalize(
        "NFD",
        texto,
    )

    return "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )


def classificar_documento(texto: str) -> str:
    """
    Classifica o documento de acordo com o tipo
    identificado no início do conteúdo.

    Categorias:
    - Lei
    - Portaria
    - Resolução
    - Outro
    """

    amostra = normalizar_texto(
        texto[:3000]
    )

    padroes = {
        "Lei": r"(?m)^\s*lei\b",
        "Portaria": r"(?m)^\s*portaria\b",
        "Resolução": r"(?m)^\s*resolucao\b",
    }

    correspondencias = []

    for tipo_documento, padrao in padroes.items():

        correspondencia = re.search(
            padrao,
            amostra,
        )

        if correspondencia:
            correspondencias.append(
                (
                    correspondencia.start(),
                    tipo_documento,
                )
            )

    if not correspondencias:
        return "Outro"

    correspondencias.sort(
        key=lambda item: item[0]
    )

    return correspondencias[0][1]