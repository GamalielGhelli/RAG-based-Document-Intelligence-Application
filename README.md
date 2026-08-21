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

### 2. Instalando o UV e suas dependências

Como instalar o `uv` no Windows:
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Com o `uv` instalado:

```bash
uv sync
```

### 3. Instalar o Ollama

Instalando o Ollama em sua máquina e confirmando a instalação:

### 4. Instalando e verificando a versão:

```bash
irm https://ollama.com/install.ps1 | iex
```

```bash
ollama --version
```

### 5. Baixar os modelos utilizados

```bash
ollama pull gemma3:1b
ollama pull embeddinggemma
```

Para conferir:

```bash
ollama list
```

### 6. Adicionar os PDFs

Os documentos devem estar na pasta:

```text
data/pdfs/
```

### 7. Executar a aplicação

```bash
uv run streamlit run app.py
```

## Observação

PDFs que não possuem camada de texto, como documentos totalmente escaneados, podem não ser processados nesta versão do projeto.

## Documentações usadas:

 Link de acesso a documentações.

- [UV](https://docs.astral.sh/uv/getting-started/installation/)
- [Ollama Embeddings](https://docs.ollama.com/capabilities/embeddings)
- [Ollama gemma3:1b](https://ollama.com/library/gemma3:1b)
- [Numpy](https://numpy.org/doc/stable/reference/generated/numpy.dot.html)
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/the-basics.html#extract-text-from-a-pdf)