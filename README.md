# Consulta Inteligente de Documentos PDF

Aplicação em Python desenvolvida para leitura, classificação, busca e consulta de documentos PDF utilizando modelos de Inteligência Artificial executados localmente.

## Objetivo

O projeto tem como objetivo:

* extrair texto de arquivos PDF;
* classificar automaticamente os documentos;
* permitir buscas em linguagem natural;
* permitir perguntas e geração de resumos através de um modelo de linguagem local.

## Tecnologias utilizadas

* **Python** — linguagem principal do projeto.
* **uv** — gerenciamento do ambiente e dependências.
* **PyMuPDF** — leitura e extração de texto dos PDFs.
* **Ollama** — execução local dos modelos de IA.
* **Gemma 3 1B** — classificação, perguntas e resumos.
* **EmbeddingGemma** — geração de embeddings para busca semântica.
* **NumPy** — cálculo de similaridade entre embeddings.
* **Streamlit** — interface da aplicação.

## Como executar

### 1. Clonar o repositório

```bash
git clone git@github.com:GamalielGhelli/estudo-caso.git
cd estudo-caso
```

### 2. Instalar as dependências

Com o `uv` instalado:

```bash
uv sync
```

### 3. Instalar o Ollama

Instale o Ollama em sua máquina e confirme a instalação:

```bash
ollama --version
```

### 4. Baixar os modelos utilizados

```bash
ollama pull gemma3:1b
ollama pull embeddinggemma
```

Para conferir:

```bash
ollama list
```

### 5. Adicionar os PDFs

Os documentos devem estar na pasta:

```text
data/pdfs/
```

### 6. Executar a aplicação

```bash
uv run streamlit run app.py
```

A aplicação ficará disponível localmente, normalmente em:

```text
http://localhost:8501
```

## Observação

PDFs que não possuem camada de texto, como documentos totalmente escaneados, podem não ser processados nesta versão do projeto.
