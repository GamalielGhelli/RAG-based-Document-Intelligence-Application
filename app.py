import streamlit as st

from estudo_caso.chat import ask_document
from estudo_caso.classifier import classify_document
from estudo_caso.pdf_reader import extract_text, find_pdfs
from estudo_caso.search import create_embedding, search_documents

st.set_page_config(
    page_title="Consulta Inteligente de PDFs",
    page_icon="📄",
    layout="wide",
)


@st.cache_data
def load_documents() -> list[dict]:
    """
    Carrega os PDFs, extrai seus textos,
    classifica os documentos e gera seus embeddings.
    """

    documents = []

    pdf_files = find_pdfs("data/pdfs")

    for pdf in pdf_files:
        text = extract_text(pdf)

        print(
            f"[DEBUG] {pdf.name}: "
            f"{len(text)} caracteres extraídos"
        )

        if not text.strip():
            documents.append(
                {
                    "name": pdf.name,
                    "path": str(pdf),
                    "text": "",
                    "type": "Não processado",
                    "embedding": None,
                    "status": "PDF sem texto extraível",
                }
            )

            continue

        document_type = classify_document(text)

        embedding = create_embedding(text)

        documents.append(
            {
                "name": pdf.name,
                "path": str(pdf),
                "text": text,
                "type": document_type,
                "embedding": embedding,
                "status": "Processado",
            }
        )

    return documents


# =================================================
# TÍTULO
# =================================================

st.title("Consulta Inteligente de Documentos PDF")

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

with st.spinner("Processando documentos..."):
    documents = load_documents()


if not documents:
    st.warning(
        "Nenhum arquivo PDF foi encontrado em data/pdfs."
    )

    st.stop()


st.success(
    f"{len(documents)} documentos carregados."
)


# =================================================
# 1. CLASSIFICAÇÃO
# =================================================

st.header("1. Documentos e classificação")


classification_data = []

for document in documents:
    classification_data.append(
        {
            "Documento": document["name"],
            "Tipo": document["type"],
            "Status": document["status"],
        }
    )


st.dataframe(
    classification_data,
    width="stretch",
)


# =================================================
# 2. BUSCA SEMÂNTICA
# =================================================

st.header("2. Busca por linguagem natural")


search_query = st.text_input(
    "Digite o que deseja encontrar:",
    placeholder="Ex: documentos relacionados à educação",
)


if st.button("Buscar documentos"):

    if not search_query.strip():
        st.warning(
            "Digite uma consulta antes de buscar."
        )

    else:
        results = search_documents(
            search_query,
            documents,
        )

        st.subheader(
            "Documentos mais relevantes"
        )

        for position, result in enumerate(
            results,
            start=1,
        ):
            st.write(
                f"""
                **{position}. {result['name']}**

                Tipo: {result['type']}

                Similaridade: {result['score']:.3f}
                """
            )


# =================================================
# 3. CHAT
# =================================================

st.header("3. Chat com o documento")


# Apenas documentos que possuem texto podem
# ser utilizados no chat.
chat_documents = [
    document
    for document in documents
    if document["text"].strip()
]


if not chat_documents:
    st.warning(
        "Nenhum documento com texto disponível para o chat."
    )

    st.stop()


document_names = [
    document["name"]
    for document in chat_documents
]


selected_name = st.selectbox(
    "Selecione o documento:",
    document_names,
)


selected_document = next(
    document
    for document in chat_documents
    if document["name"] == selected_name
)


# Se o usuário mudar de documento,
# limpa o histórico do chat.
if (
    "selected_document" not in st.session_state
    or st.session_state.selected_document != selected_name
):
    st.session_state.selected_document = selected_name
    st.session_state.messages = []


if "messages" not in st.session_state:
    st.session_state.messages = []


# Exibe histórico
for message in st.session_state.messages:
    with st.chat_message(
        message["role"]
    ):
        st.write(
            message["content"]
        )


# Campo de pergunta
question = st.chat_input(
    "Faça uma pergunta sobre o documento..."
)


if question:

    previous_history = (
        st.session_state.messages.copy()
    )

    # Salva pergunta
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Mostra pergunta
    with st.chat_message("user"):
        st.write(question)

    # Gera resposta
    with st.chat_message("assistant"):

        with st.spinner(
            "Analisando documento..."
        ):
            answer = ask_document(
                selected_document["text"],
                question,
                previous_history,
            )

        st.write(answer)

    # Salva resposta
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )