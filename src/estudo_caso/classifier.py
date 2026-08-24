import re
import unicodedata


def normalize_text(text: str) -> str:
    """
    Normaliza o texto:
    - transforma em minúsculas
    - remove acentos
    """

    text = text.casefold()

    text = unicodedata.normalize(
        "NFD",
        text,
    )

    return "".join(
        character
        for character in text
        if unicodedata.category(character) != "Mn"
    )


def classify_document(text: str) -> str:
    """
    Classifica o documento de acordo com o primeiro
    tipo documental encontrado no início do conteúdo.

    Categorias:
    - Lei
    - Portaria
    - Resolução
    - Outro
    """

    # Para identificar o tipo do documento,
    # o início normalmente é suficiente.
    sample = normalize_text(text[:3000])

    patterns = {
        "Lei": r"\blei\b",
        "Portaria": r"\bportaria\b",
        "Resolução": r"\bresolucao\b",
    }

    matches = []

    for document_type, pattern in patterns.items():
        match = re.search(pattern, sample)

        if match:
            matches.append(
                (
                    match.start(),
                    document_type,
                )
            )

    if not matches:
        return "Outro"

    # Ordena pela posição em que a palavra apareceu
    # no documento.
    matches.sort(
        key=lambda item: item[0]
    )

    return matches[0][1]