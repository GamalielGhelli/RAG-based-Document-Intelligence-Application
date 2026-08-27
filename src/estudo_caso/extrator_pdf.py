from pathlib import Path

import pymupdf

IDIOMA_OCR = "por"
DPI_OCR = 300


def encontrar_pdfs(
    diretorio: str = "data/pdfs",
) -> list[Path]:
    """
    Procura todos os arquivos PDF
    existentes no diretório informado.
    """

    caminho = Path(diretorio)

    return sorted(
        caminho.glob("*.pdf")
    )


def extrair_texto(
    caminho_pdf: str | Path,
) -> tuple[str, str]:


    partes_texto = []

    usou_texto_nativo = False
    usou_ocr = False

    with pymupdf.open(
        caminho_pdf
    ) as documento:

        for pagina in documento:

            texto = pagina.get_text(
                "text",
                sort=True,
            )

            # Se a página já possui texto,
            # utiliza a extração normal.
            if texto.strip():

                usou_texto_nativo = True

            # Caso contrário, tenta OCR.
            else:

                pagina_texto = (
                    pagina.get_textpage_ocr(
                        language=IDIOMA_OCR,
                        dpi=DPI_OCR,
                        full=True,
                    )
                )

                texto = pagina.get_text(
                    "text",
                    textpage=pagina_texto,
                    sort=True,
                )

                if texto.strip():
                    usou_ocr = True

            if texto.strip():

                partes_texto.append(
                    texto.strip()
                )

    texto_completo = "\n\n".join(
        partes_texto
    )

    # Define como o documento foi processado.
    if usou_texto_nativo and usou_ocr:

        metodo_extracao = (
            "PyMuPDF + OCR"
        )

    elif usou_ocr:

        metodo_extracao = "OCR"

    elif usou_texto_nativo:

        metodo_extracao = "PyMuPDF"

    else:

        metodo_extracao = (
            "Não extraído"
        )

    return (
        texto_completo,
        metodo_extracao,
    )