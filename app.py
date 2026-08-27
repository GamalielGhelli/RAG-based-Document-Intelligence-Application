import streamlit as st

from estudo_caso.busca_semantica import buscar_documentos, criar_embedding
from estudo_caso.chat import perguntar_documento
from estudo_caso.classificador import classificar_documento
from estudo_caso.extrator_pdf import encontrar_pdfs, extrair_texto

st.set_page_config(
    page_title="Consulta Inteligente de PDFs",
    page_icon="📄",
    layout="wide",
)

@st.cache_data
def carregar_documentos() -> list[dict]:
    """
    Carrega os PDFs, extrai seus textos,
    classifica os documentos e gera seus embeddings.
    """

    documentos = []

    arquivos_pdf = encontrar_pdfs(
        "data/pdfs"
    )

    for pdf in arquivos_pdf:

        texto, metodo_extracao = (
            extrair_texto(pdf)
        )

        print(
            f"[DEBUG] {pdf.name}: "
            f"{len(texto)} caracteres extraídos "
            f"usando {metodo_extracao}"
        )

        if not texto.strip():

            documentos.append(
                {
                    "nome": pdf.name,
                    "caminho": str(pdf),
                    "texto": "",
                    "tipo": "Não processado",
                    "metodo_extracao": metodo_extracao,
                    "embedding": None,
                    "status": "PDF sem texto extraível",
                }
            )

            continue

        tipo_documento = (
            classificar_documento(
                texto
            )
        )

        embedding = criar_embedding(
            texto
        )

        documentos.append(
            {
                "nome": pdf.name,
                "caminho": str(pdf),
                "texto": texto,
                "tipo": tipo_documento,
                "metodo_extracao": metodo_extracao,
                "embedding": embedding,
                "status": "Processado",
            }
        )

    return documentos

# =================================================
# TÍTULO
# =================================================

st.title(
    "Consulta Inteligente de Documentos PDF"
)

st.write(
    """
    Aplicação para extração, classificação,
    busca semântica e consulta de documentos PDF
    utilizando modelos executados localmente.
    """
)

# =================================================
# CARREGAMENTO DOS DOCUMENTOS
# =================================================

with st.spinner(
    "Processando documentos..."
):

    documentos = carregar_documentos()

if not documentos:

    st.warning(
        "Nenhum arquivo PDF foi encontrado em data/pdfs."
    )

    st.stop()

st.success(
    f"{len(documentos)} documentos carregados."
)

# =================================================
# 1. CLASSIFICAÇÃO
# =================================================

st.header(
    "1. Documentos e classificação"
)

quantidade_ocr = sum(
    1
    for documento in documentos
    if "OCR"
    in documento["metodo_extracao"]
)

st.caption(
    f"OCR utilizado em "
    f"{quantidade_ocr} documento(s)."
)

dados_classificacao = []

for documento in documentos:

    dados_classificacao.append(
        {
            "Documento": documento[
                "nome"
            ],
            "Tipo": documento[
                "tipo"
            ],
            "Extração": documento[
                "metodo_extracao"
            ],
            "Status": documento[
                "status"
            ],
        }
    )


st.dataframe(
    dados_classificacao,
    width="stretch",
    hide_index=True,
)

# =================================================
# 2. BUSCA SEMÂNTICA
# =================================================

st.header(
    "2. Busca por linguagem natural"
)

consulta_busca = st.text_input(
    "Digite o que deseja encontrar:",
    placeholder=(
        "Ex: documentos relacionados à educação"
    ),
)

if st.button(
    "Buscar documentos"
):

    if not consulta_busca.strip():

        st.warning(
            "Digite uma consulta antes de buscar."
        )

    else:

        resultados = buscar_documentos(
            consulta_busca,
            documentos,
        )

        st.subheader(
            "Documentos mais relevantes"
        )

        for posicao, resultado in enumerate(
            resultados,
            start=1,
        ):

            st.write(
                f"""
                **{posicao}. {resultado['nome']}**

                Tipo: {resultado['tipo']}

                Similaridade: {resultado['similaridade']:.3f}
                """
            )

# =================================================
# 3. CHAT
# =================================================

@st.fragment
def exibir_chat(
    documentos: list[dict],
) -> None:
    """
    Exibe o chat com os documentos.

    O fragment permite atualizar somente
    esta parte da aplicação durante a conversa.
    """

    st.header(
        "3. Chat com o documento"
    )

    documentos_chat = [
        documento
        for documento in documentos
        if documento["texto"].strip()
    ]

    if not documentos_chat:

        st.warning(
            "Nenhum documento com texto "
            "disponível para o chat."
        )

        return

    nomes_documentos = [
        documento["nome"]
        for documento in documentos_chat
    ]

    nome_selecionado = st.selectbox(
        "Selecione o documento:",
        nomes_documentos,
        key="seletor_documento",
    )

    documento_selecionado = next(
        documento
        for documento in documentos_chat
        if documento["nome"]
        == nome_selecionado
    )

    # Se o usuário trocar de documento,
    # limpa o histórico da conversa.
    if (
        "documento_selecionado"
        not in st.session_state
        or
        st.session_state.documento_selecionado
        != nome_selecionado
    ):

        st.session_state.documento_selecionado = (
            nome_selecionado
        )

        st.session_state.mensagens = []

    if (
        "mensagens"
        not in st.session_state
    ):

        st.session_state.mensagens = []

    for mensagem in (
        st.session_state.mensagens
    ):

        with st.chat_message(
            mensagem["role"]
        ):

            st.write(
                mensagem["content"]
            )

    pergunta = st.chat_input(
        "Faça uma pergunta sobre o documento...",
        key="entrada_chat",
    )

    if pergunta:

        historico_anterior = (
            st.session_state
            .mensagens
            .copy()
        )

        # Salva a pergunta no histórico.
        st.session_state.mensagens.append(
            {
                "role": "user",
                "content": pergunta,
            }
        )

        # Mostra temporariamente
        # a nova pergunta.
        with st.chat_message(
            "user"
        ):

            st.write(
                pergunta
            )

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Analisando documento..."
            ):

                resposta = perguntar_documento(
                    documento_selecionado[
                        "texto"
                    ],
                    pergunta,
                    historico_anterior,
                )

            st.write(
                resposta
            )

        # Salva a resposta no histórico.
        st.session_state.mensagens.append(
            {
                "role": "assistant",
                "content": resposta,
            }
        )

        # Recarrega somente o fragmento.
        #
        # Isso faz com que todas as mensagens
        # sejam desenhadas novamente antes
        # do campo de entrada.
        st.rerun(
            scope="fragment"
        )

# Exibe o chat.
exibir_chat(
    documentos
)