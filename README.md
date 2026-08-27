# Aplicativo de Inteligência de Documentos

Aplicação em Python para extração, classificação, busca semântica e consulta de documentos PDF utilizando modelos de Inteligência Artificial executados localmente.

O projeto foi desenvolvido como estudo de caso para demonstrar uma solução capaz de:

* extrair texto de arquivos PDF;
* classificar automaticamente documentos por tipo;
* permitir buscas em linguagem natural;
* retornar documentos relevantes com base na consulta do usuário;
* permitir perguntas e geração de resumos com apoio de uma LLM local.

## Objetivo do projeto

O objetivo principal é criar um MVP funcional para consulta inteligente de documentos PDF.

A aplicação recebe documentos em PDF, extrai o conteúdo textual, identifica o tipo do documento, gera representações vetoriais para busca semântica e permite interação com um modelo de linguagem local para perguntas e resumos.

A solução foi pensada para rodar localmente, sem necessidade de GPU, utilizando modelos leves via Ollama.

## Funcionalidades

* Leitura automática dos arquivos PDF da pasta `data/pdfs/`;
* Extração de texto com PyMuPDF + Fallback com OCR quando uma página não possui camada textual extraível;
* Classificação automática em categorias como Lei, Portaria, Resolução ou Outro;
* Geração de embeddings para busca semântica;
* Busca por linguagem natural;
* Retorno dos documentos mais relevantes;
* Chat com documento selecionado;
* Geração de respostas e resumos com LLM local;
* Interface web simples com Streamlit.

## Estrutura do projeto

```text
.
├── data/
│   └── pdfs/
├── src/
│   └── estudo_caso/
│       ├── busca_semantica.py
│       ├── chat.py
│       ├── classificador.py
│       └── extrator_pdf.py
├── tests/
├── app.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Explicação dos principais arquivos

### `app.py`

Arquivo principal da aplicação.

Ele integra todos os módulos do projeto e cria a interface com Streamlit.
É responsável por:

* carregar os PDFs;
* extrair os textos;
* classificar os documentos;
* gerar embeddings;
* exibir a tabela de documentos processados;
* executar a busca semântica;
* exibir o chat com o documento selecionado.

### `extrator_pdf.py`

Responsável por encontrar e extrair texto dos PDFs.

Fluxo:

1. procura arquivos `.pdf` na pasta `data/pdfs/`;
2. tenta extrair o texto diretamente com PyMuPDF;
3. caso uma página não tenha texto, tenta utilizar OCR;
4. retorna o texto extraído e o método utilizado.

Métodos possíveis:

* `PyMuPDF`;
* `OCR`;
* `PyMuPDF + OCR`;
* `Não extraído`.

### `classificador.py`

Responsável por classificar o tipo do documento.

A classificação foi feita por regras simples, utilizando expressões regulares.
Essa escolha foi feita porque os documentos possuem padrões textuais claros no início do conteúdo, como:

* Lei;
* Portaria;
* Resolução.

Antes da classificação, o texto é normalizado para facilitar a comparação:

* transforma o texto em minúsculas;
* remove acentos;
* analisa o início do documento.

Caso nenhum padrão seja encontrado, o documento é classificado como `Outro`.

### `busca_semantica.py`

Responsável pela busca em linguagem natural.

Fluxo:

1. transforma o texto dos documentos em embeddings;
2. transforma a pergunta do usuário em embedding;
3. compara a pergunta com os documentos usando similaridade de cosseno;
4. ordena os resultados;
5. retorna os documentos mais relevantes.

A busca semântica permite encontrar documentos relacionados ao significado da pergunta, mesmo quando o usuário não utiliza exatamente as mesmas palavras presentes no PDF.

### `chat.py`

Responsável pela interação com a LLM local.

O conteúdo do documento selecionado é enviado como contexto para o modelo `gemma3:1b`.

O modelo é instruído a responder apenas com base no documento informado.
Caso a informação não esteja no conteúdo, ele deve informar que não foi possível encontrá-la.

Também é possível pedir resumos objetivos dos documentos.

## Tecnologias utilizadas

### Python

Linguagem principal do projeto.

Foi escolhida por ter bom suporte para manipulação de arquivos, processamento de texto, bibliotecas de IA e criação rápida de aplicações.

### uv

Ferramenta utilizada para gerenciamento do ambiente Python e das dependências.

Ela facilita a instalação das bibliotecas necessárias e a reprodução do ambiente do projeto.

### Streamlit

Biblioteca utilizada para criar a interface web da aplicação.

Foi escolhida por permitir criar uma interface funcional de forma simples e rápida, ideal para demonstração de MVPs e estudos de caso.

### PyMuPDF

Biblioteca utilizada para leitura e extração de texto dos arquivos PDF.

Também foi utilizada para tentar OCR em páginas que não possuem texto extraível diretamente.

### Ollama

Ferramenta utilizada para executar modelos de IA localmente.

Permite rodar tanto o modelo de linguagem quanto o modelo de embeddings na máquina do usuário, sem depender de uma API externa.

### Gemma 3 1B

Modelo de linguagem utilizado para responder perguntas e gerar resumos dos documentos.

Foi escolhido por ser um modelo leve, adequado para execução local e suficiente para o escopo do estudo de caso.

### EmbeddingGemma

Modelo utilizado para gerar embeddings dos documentos e das consultas do usuário.

Esses embeddings são vetores numéricos que representam semanticamente os textos, permitindo realizar busca por significado.

### NumPy

Biblioteca utilizada para operações matemáticas com vetores.

Neste projeto, foi usada principalmente para calcular a similaridade de cosseno entre embeddings.

## Requisitos

* Python 3.12 ou superior;
* uv instalado;
* Ollama instalado e em execução;
* Modelos `gemma3:1b` e `embeddinggemma` baixados no Ollama;
* PDFs disponíveis na pasta `data/pdfs/`.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone git@github.com:GamalielGhelli/RAG-based-Document-Intelligence-Application.git
cd RAG-based-Document-Intelligence-Application
```

### 2. Instalar o uv

No Windows, execute o PowerShell como administrador:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Depois, confira se a instalação funcionou:

```bash
uv --version
```

### 3. Instalar as dependências do projeto

```bash
uv sync
```

Esse comando cria o ambiente virtual e instala as bibliotecas definidas no `pyproject.toml`.

### 4. Instalando o Tesseract-ocr

Nesta documentação você encontrará o executável do [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki), após a intalação você deverá clicar no executavel, apenas escolher o idioma e seguir até a instalação seja concluída.

### 5. Instalar o Ollama

No Windows, execute o PowerShell como administrador:

```bash
irm https://ollama.com/install.ps1 | iex
```

Depois, confira se o Ollama foi instalado:

```bash
ollama --version
```

Também é importante garantir que o Ollama esteja em execução antes de abrir a aplicação.

### 6. Baixar os modelos utilizados

```bash
ollama pull gemma3:1b
ollama pull embeddinggemma
```

Para verificar se os modelos foram baixados:

```bash
ollama list
```

### 7. Adicionar os PDFs

Os arquivos PDF devem estar dentro da pasta:

```text
data/pdfs/
```

### 8. Executar a aplicação

```bash
uv run streamlit run app.py
```

Após executar o comando, o Streamlit abrirá a aplicação no navegador.

## Como usar a aplicação

### 1. Documentos e classificação

Ao iniciar, a aplicação carrega os PDFs da pasta `data/pdfs/`.

Em seguida, exibe uma tabela com:

* nome do documento;
* tipo identificado;
* método de extração utilizado;
* status do processamento.

### 2. Busca por linguagem natural

O usuário pode digitar uma pergunta ou termo de busca.

Exemplo:

```text
documentos relacionados à educação
```

A aplicação gera o embedding da consulta, compara com os embeddings dos documentos e retorna os documentos mais relevantes.

### 3. Chat com documento

O usuário seleciona um documento e pode fazer perguntas sobre ele.

Exemplos:

```text
Faça um resumo deste documento.
```

```text
Qual é o principal objetivo deste documento?
```

```text
Este documento fala sobre educação?
```

A resposta é gerada com base no conteúdo do documento selecionado.

## Decisões técnicas

### Por que usar busca semântica?

A busca semântica permite encontrar documentos pelo significado da consulta, e não apenas pela presença exata de palavras.

Isso é útil porque o usuário pode fazer perguntas em linguagem natural, sem conhecer os termos exatos usados no documento.

### Por que usar embeddings?

Embeddings representam textos como vetores numéricos.

Com esses vetores, é possível comparar a proximidade semântica entre a consulta do usuário e os documentos processados.

### Por que usar similaridade de cosseno?

A similaridade de cosseno mede o quanto dois vetores apontam para direções semelhantes.

Neste projeto, ela foi usada para comparar o embedding da pergunta com o embedding de cada documento.

Quanto maior a similaridade, mais relevante o documento tende a ser para a consulta.

### Por que não usar banco vetorial?

Como o estudo de caso possui apenas 10 PDFs, não foi necessário utilizar ferramentas como FAISS, ChromaDB ou outro banco vetorial.

Os embeddings são mantidos em memória durante a execução da aplicação, e a comparação com NumPy é suficiente para o volume de documentos utilizado.

Em um cenário com milhares de documentos, uma evolução natural seria adicionar:

* divisão dos documentos em chunks;
* armazenamento vetorial;
* busca por trechos mais relevantes;
* pipeline RAG mais completo.

### O projeto é um RAG completo?

O projeto utiliza conceitos presentes em arquiteturas RAG, como extração de documentos, embeddings, recuperação semântica e geração de respostas com LLM.

No entanto, para manter o MVP simples e adequado ao escopo do estudo de caso, a busca semântica e o chat foram mantidos como funcionalidades separadas.

Uma evolução futura seria integrar diretamente os resultados da busca ao contexto enviado para a LLM.

## Limitações

* Os embeddings são gerados com uma amostra inicial do texto do documento.
* O chat utiliza uma quantidade limitada de caracteres do documento como contexto.
* A classificação foi feita para os tipos identificados no estudo de caso.
* O OCR pode depender da configuração local do ambiente.
* Para grandes volumes de documentos, seria recomendado implementar chunking e banco vetorial.

## Possíveis melhorias futuras

* Implementar chunking dos documentos;
* Utilizar banco vetorial como FAISS ou ChromaDB;
* Permitir upload de PDFs pela interface;
* Salvar embeddings para evitar reprocessamento;
* Melhorar o tratamento de documentos muito grandes;
* Criar testes automatizados mais completos;
* Adicionar logs estruturados;
* Exportar respostas ou resumos gerados.

## Documentações utilizadas

* [UV](https://docs.astral.sh/uv/getting-started/installation/)
* [Ollama](Embeddingshttps://docs.ollama.com/capabilities/embeddings)
* [Ollama-Gemma3:1b](https://ollama.com/library/gemma3:1b)
* [NumPy](https://numpy.org/doc/stable/reference/generated/numpy.dot.html)
* [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/the-basics.html#extract-text-from-a-pdf)
* [Streamli](thttps://docs.streamlit.io/)
