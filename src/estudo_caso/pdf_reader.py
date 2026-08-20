from pathlib import Path

import pymupdf


def find_pdfs(directory: str = "data/pdfs") -> list[Path]:
    """Retorna todos os arquivos PDF encontrados no diretório informado."""

    path = Path(directory)
    return sorted(path.glob("*.pdf"))


def extract_text(pdf_path: str | Path) -> str:
    """Extrai todo o texto de um arquivo PDF."""

    text_parts = []
    with pymupdf.open(pdf_path) as document:
        for page in document:
            text = page.get_text("text", sort=True)

            if text.strip():
                text_parts.append(text.strip())
    return "\n\n".join(text_parts)