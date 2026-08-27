from estudo_caso.busca_semantica import buscar_documentos, criar_embedding
from estudo_caso.extrator_pdf import encontrar_pdfs, extrair_texto


def carregar_documentos_teste():
    """
    Prepara os documentos necessários
    para testar a busca semântica.
    """

    documentos = []

    arquivos_pdf = encontrar_pdfs(
        "data/pdfs"
    )

    for pdf in arquivos_pdf:

        texto, _ = extrair_texto(
            pdf
        )

        if not texto.strip():
            continue

        embedding = criar_embedding(
            texto
        )

        documentos.append(
            {
                "nome": pdf.name,
                "tipo": "",
                "embedding": embedding,
            }
        )

    return documentos


def testar_busca():
    """
    Executa algumas consultas conhecidas
    e verifica se o primeiro resultado
    é o documento esperado.
    """

    documentos = (
        carregar_documentos_teste()
    )

    casos_teste = {
        "regras do ensino médio":
            "Lei_14945_31072024.pdf",

        "fiscalização de trânsito por câmeras":
            "Resolucao_909_28032022.pdf",

        "perícia médica":
            "Resolucao_2430_21052025.pdf",

        "Bolsa Família e Cadastro Único":
            "Portaria_81_25082015.pdf",

        "controle patrimonial":
            "Portaria_44_28052025.pdf",
    }

    acertos = 0

    for consulta, documento_esperado in (
        casos_teste.items()
    ):

        resultados = buscar_documentos(
            consulta,
            documentos,
            quantidade_resultados=3,
        )

        primeiro_resultado = (
            resultados[0]["nome"]
        )

        acertou = (
            primeiro_resultado
            == documento_esperado
        )

        if acertou:
            acertos += 1

        print()
        print(
            f"Consulta: {consulta}"
        )

        print(
            f"Esperado: "
            f"{documento_esperado}"
        )

        print(
            f"Encontrado: "
            f"{primeiro_resultado}"
        )

        print(
            "Resultado: "
            + (
                "ACERTO"
                if acertou
                else "ERRO"
            )
        )

    total_testes = len(
        casos_teste
    )

    print()
    print(
        "=========================="
    )

    print(
        f"Resultado final: "
        f"{acertos}/{total_testes}"
    )

    print(
        "=========================="
    )


if __name__ == "__main__":
    testar_busca()