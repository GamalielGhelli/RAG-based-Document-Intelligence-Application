# Consulta Inteligente de Documentos PDF

Aplicação desenvolvida em Python para **extração, classificação, busca semântica e consulta de documentos PDF utilizando modelos de linguagem executados localmente**.

O projeto foi desenvolvido como estudo de caso para uma vaga de **Estágio em Dados e Inteligência Artificial**, com foco na criação de uma solução simples e funcional para processamento e consulta inteligente de documentos.

---

## Objetivo

O objetivo da aplicação é permitir o processamento automático de documentos PDF e oferecer recursos de consulta utilizando técnicas de Inteligência Artificial.

A solução busca atender aos seguintes requisitos:

1. Ler e extrair texto de documentos PDF.
2. Classificar automaticamente cada documento de acordo com seu tipo.
3. Permitir buscas utilizando linguagem natural e retornar os documentos mais relevantes.
4. Permitir interação com um modelo de linguagem para:

   * responder perguntas sobre os documentos;
   * gerar resumos;
   * auxiliar na interpretação do conteúdo.

A aplicação foi desenvolvida para funcionar **localmente**, utilizando modelos leves que podem ser executados sem exigir uma GPU dedicada.

---

## Funcionalidades

### Extração de texto

Os documentos armazenados em `data/pdfs` são automaticamente identificados e processados utilizando **PyMuPDF**.

O conteúdo textual de cada página é extraído e utilizado nas demais etapas do sistema.

### Classificação automática

Após a extração, o conteúdo do documento é enviado para um modelo de linguagem local executado através do **Ollama**.

Atualmente os documentos são classificados nas seguintes categorias:

* Lei
* Portaria
* Resolução
* Outro

A classificação é feita utilizando o **conteúdo do documento**, e não apenas o nome do arquivo.

### Busca por linguagem natural

A aplicação permite realizar pesquisas utilizando frases comuns, por exemplo:

```text
documentos relacionados à educação
```

ou:

```text
normas relacionadas a processos administrativos
```

Cada documento é convertido em uma representação vetorial chamada **embedding**.

A consulta do usuário também é transformada em um embedding e comparada com os documentos utilizando **similaridade cosseno**.

Os documentos com maior similaridade são apresentados primeiro.

### Chat com os documentos

O usuário pode selecionar um documento e realizar perguntas como:

```text
Qual é o objetivo principal deste documento?
```

```text
Faça um resumo dos principais pontos.
```

```text
O que este documento determina sobre educação básica?
```

O conteúdo do documento é fornecido como contexto para o modelo de linguagem, permitindo que a resposta seja baseada no arquivo selecionado.

---

# Arquitetura

O fluxo simplificado da aplicação é:

```text
                  PDFs
                   │
                   ▼
               PyMuPDF
                   │
                   ▼
            Extração de texto
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
     Classificação       Embedding
        Ollama          EmbeddingGemma
          │                 │
          │                 ▼
          │               NumPy
          │         Similaridade cosseno
          │                 │
          │                 ▼
          │          Busca semântica
          │
          ▼
     Gemma 3 1B
          │
          ▼
     Chat / Resumo
          │
          ▼
       Streamlit
```

---

# Tecnologias utilizadas

## Python

Linguagem principal utilizada no desenvolvimento da aplicação.

Foi escolhida devido ao seu amplo ecossistema para:

* processamento de documentos;
* Inteligência Artificial;
* Machine Learning;
* manipulação de dados;
* integração com modelos de linguagem.

---

## uv

O **uv** é utilizado para gerenciamento do projeto Python.

Ele é responsável por:

* criação e gerenciamento do ambiente virtual;
* instalação das dependências;
* gerenciamento do `pyproject.toml`;
* geração do `uv.lock`;
* execução dos comandos dentro do ambiente do projeto.

Isso permite que o ambiente seja reproduzido com maior facilidade em outras máquinas.

---

## PyMuPDF

Biblioteca utilizada para leitura dos arquivos PDF e extração do conteúdo textual.

O processo utilizado pela aplicação é basicamente:

```text
PDF
 ↓
abrir documento
 ↓
percorrer páginas
 ↓
extrair texto
```

O PyMuPDF foi escolhido por possuir uma API simples e permitir acessar o conteúdo dos documentos página por página.

---

## Ollama

O **Ollama** é utilizado para executar modelos de Inteligência Artificial localmente.

Isso evita a necessidade de enviar os documentos para APIs externas e atende ao objetivo de executar a solução localmente.

Dois modelos são utilizados na aplicação.

### Gemma 3 1B

Modelo utilizado para:

* classificação dos documentos;
* respostas no chat;
* geração de resumos.

Foi escolhido por ser um modelo relativamente pequeno e adequado para execução em máquinas sem GPU dedicada.

### EmbeddingGemma

Modelo utilizado para gerar os embeddings necessários para a busca semântica.

Ele transforma textos em vetores numéricos que representam semanticamente seu conteúdo.

---

## NumPy

O NumPy é utilizado para realizar operações matemáticas com os embeddings.

A principal operação utilizada é a **similaridade cosseno**.

De forma simplificada:

```text
Pergunta
   ↓
Embedding
   ↓
Comparação com embeddings dos documentos
   ↓
Pontuação de similaridade
   ↓
Documentos mais relevantes
```

Como o estudo de caso possui apenas uma pequena quantidade de documentos, foi possível realizar essa comparação diretamente com NumPy sem a necessidade de utilizar um banco de dados vetorial.

---

## Streamlit

O Streamlit é utilizado para criar a interface da aplicação.

A interface apresenta três funcionalidades principais:

```text
1. Documentos e classificação

2. Busca por linguagem natural

3. Chat com o documento
```

A escolha do Streamlit permitiu desenvolver uma interface funcional utilizando apenas Python, mantendo o foco principal do projeto na parte de processamento de documentos e Inteligência Artificial.

---

# Estrutura do projeto

```text
estudo-caso/
│
├── data/
│   ├── pdfs/
│   │   ├── documentos.pdf
│   │   └── ...
│   │
│   └── processed/
│
├── src/
│   └── estudo_caso/
│       ├── __init__.py
│       ├── pdf_reader.py
│       ├── classifier.py
│       ├── search.py
│       └── chat.py
│
├── tests/
│   └── test_pdf_reader.py
│
├── app.py
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

---

# Responsabilidade dos arquivos

## `app.py`

Ponto de entrada da aplicação.

Responsável por:

* carregar os documentos;
* organizar a interface Streamlit;
* exibir as classificações;
* receber consultas;
* mostrar resultados da busca;
* controlar o chat.

---

## `pdf_reader.py`

Responsável pela leitura dos documentos PDF.

Principais responsabilidades:

```text
Encontrar PDFs
      ↓
Abrir documentos
      ↓
Extrair texto
```

---

## `classifier.py`

Responsável pela classificação automática dos documentos utilizando o modelo de linguagem executado pelo Ollama.

Fluxo:

```text
Texto do documento
        ↓
    Gemma 3 1B
        ↓
Lei / Portaria / Resolução / Outro
```

---

## `search.py`

Responsável pela busca semântica.

Realiza:

* geração dos embeddings;
* geração do embedding da consulta;
* cálculo da similaridade cosseno;
* ordenação dos documentos por relevância.

---

## `chat.py`

Responsável pela interação entre o usuário e o modelo de linguagem.

O conteúdo do documento selecionado é fornecido como contexto ao modelo juntamente com a pergunta feita pelo usuário.

---

# Pré-requisitos

Para executar o projeto é necessário possuir:

* Python 3.12 ou superior;
* Git;
* uv;
* Ollama.

Também é necessário baixar os modelos utilizados pela aplicação.

---

# Instalação

## 1. Clone o repositório

```bash
git clone git@github.com:GamalielGhelli/estudo-caso.git
```

Entre no diretório:

```bash
cd estudo-caso
```

---

## 2. Instale as dependências

Com o `uv` instalado:

```bash
uv sync
```

O comando utilizará o `pyproject.toml` e o `uv.lock` para criar e sincronizar o ambiente da aplicação.

---

## 3. Instale o Ollama

Instale o Ollama no sistema operacional utilizado.

Após a instalação, confirme:

```bash
ollama --version
```

---

## 4. Baixe os modelos

Modelo utilizado para classificação e chat:

```bash
ollama pull gemma3:1b
```

Modelo utilizado para embeddings:

```bash
ollama pull embeddinggemma
```

Confira os modelos instalados:

```bash
ollama list
```

O resultado deverá incluir:

```text
gemma3:1b
embeddinggemma
```

---

## 5. Adicione os documentos

Os arquivos PDF devem estar dentro de:

```text
data/pdfs/
```

Exemplo:

```text
data/
└── pdfs/
    ├── documento_01.pdf
    ├── documento_02.pdf
    └── documento_03.pdf
```

---

# Executando o projeto

Execute:

```bash
uv run streamlit run app.py
```

O Streamlit iniciará um servidor local.

Normalmente a aplicação estará disponível em:

```text
http://localhost:8501
```

---

# Funcionamento interno

## 1. Carregamento

Ao iniciar a aplicação, os arquivos encontrados em:

```text
data/pdfs
```

são identificados automaticamente.

---

## 2. Extração

Cada PDF é aberto pelo PyMuPDF.

O sistema percorre suas páginas e extrai o conteúdo textual disponível.

```text
PDF
 ↓
Página 1
Página 2
Página 3
...
 ↓
Texto completo
```

---

## 3. Classificação

Uma amostra do conteúdo extraído é enviada ao Gemma 3 1B.

O modelo recebe instruções para classificar o documento em uma das categorias disponíveis.

```text
Documento
   ↓
Gemma 3 1B
   ↓
Tipo do documento
```

---

## 4. Geração de embeddings

Para permitir a busca semântica, o conteúdo dos documentos é enviado ao EmbeddingGemma.

O modelo transforma o texto em um vetor numérico.

Exemplo conceitual:

```text
"educação básica"

↓

[0.12, -0.53, 0.81, 0.24, ...]
```

Esses valores representam características semânticas do texto.

---

## 5. Busca semântica

Quando uma consulta é realizada:

```text
educação básica brasileira
```

ela também é transformada em embedding.

Depois, o NumPy calcula a similaridade entre:

```text
Embedding da pergunta

        X

Embedding de cada documento
```

Os resultados são ordenados pela maior similaridade.

---

## 6. Chat

No chat, o usuário seleciona um documento.

O sistema envia ao modelo:

```text
Conteúdo do documento
+
Pergunta
+
Histórico recente da conversa
```

O modelo então gera uma resposta baseada no conteúdo disponibilizado.

---

# Decisões técnicas

## Por que não utilizar banco vetorial?

O conjunto utilizado no estudo de caso possui poucos documentos.

Por esse motivo, os embeddings podem ser comparados diretamente utilizando NumPy.

Para esse cenário, adicionar tecnologias como:

* FAISS;
* Chroma;
* Pinecone;
* pgvector;

aumentaria a complexidade do projeto sem trazer benefício significativo.

Em uma solução com milhares ou milhões de documentos, um banco vetorial seria uma evolução natural.

---

## Por que não utilizar LangChain?

A solução foi implementada utilizando diretamente as bibliotecas responsáveis por cada etapa.

Isso permite visualizar de maneira mais clara o fluxo:

```text
texto
 ↓
embedding
 ↓
similaridade
 ↓
resultado
```

A utilização de frameworks como LangChain poderia simplificar algumas etapas, porém adicionaria uma camada adicional de abstração desnecessária para o escopo deste MVP.

---

## Por que utilizar modelos locais?

A utilização do Ollama permite que o processamento dos documentos seja realizado localmente.

Entre as vantagens estão:

* menor dependência de serviços externos;
* ausência de custos com API durante os testes;
* maior privacidade dos documentos;
* possibilidade de funcionamento offline após o download dos modelos.

Além disso, modelos menores permitem que a solução seja executada utilizando CPU.

---

# Limitações atuais

## PDFs escaneados

O PyMuPDF consegue extrair texto diretamente quando o documento possui uma camada textual.

Entretanto, PDFs compostos apenas por imagens podem retornar texto vazio.

Atualmente esses arquivos são identificados como:

```text
PDF sem texto extraível
```

e não são utilizados na classificação, busca ou chat.

---

## Representação por documento

Nesta versão do MVP, cada documento recebe uma representação utilizada na busca semântica.

Para documentos muito grandes, uma informação relevante localizada em uma seção específica pode ter menor influência sobre a representação geral.

---

## Modelos pequenos

O Gemma 3 1B foi escolhido principalmente pelo baixo requisito computacional.

Modelos maiores podem produzir respostas mais completas e precisas, porém exigem mais memória e processamento.

---

# Possíveis melhorias

Algumas evoluções possíveis para o projeto seriam:

### OCR

Implementar OCR para documentos escaneados utilizando ferramentas como:

* Tesseract;
* OCRmyPDF;
* OCR integrado ao PyMuPDF.

O fluxo passaria a ser:

```text
PDF
 ↓
Existe texto?
 ├── Sim → processamento normal
 │
 └── Não
      ↓
     OCR
      ↓
     Texto
```

### Divisão em chunks

Documentos maiores poderiam ser divididos em pequenos trechos.

Exemplo:

```text
Documento
 ↓
Chunk 1
Chunk 2
Chunk 3
Chunk 4
```

Cada trecho possuiria seu próprio embedding.

Isso permitiria recuperar partes específicas do documento em vez de apenas identificar o arquivo mais relevante.

### Busca por página

Os metadados poderiam armazenar:

* documento;
* página;
* trecho;
* embedding.

Assim uma pesquisa poderia retornar diretamente:

```text
Lei_9394.pdf
Página 12
```

### Banco vetorial

Para bases maiores, os embeddings poderiam ser armazenados em soluções como:

* FAISS;
* Chroma;
* pgvector;
* Qdrant.

### Modelos maiores

Em ambientes com maior capacidade computacional, modelos maiores poderiam melhorar:

* classificação;
* compreensão de contexto;
* geração de resumos;
* qualidade das respostas.

### Avaliação da busca

Também seria possível criar um conjunto de perguntas conhecidas e avaliar métricas como:

* Precision@K;
* Recall@K;
* relevância dos documentos recuperados.

### Upload de documentos

Uma evolução da interface poderia permitir que novos PDFs fossem adicionados diretamente pelo Streamlit.

---

# Testes

Os testes automatizados ficam localizados em:

```text
tests/
```

Para executá-los:

```bash
uv run pytest
```

---

# Fluxo resumido

```text
                    Usuário
                       │
                       ▼
                   Streamlit
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
   Classificação     Busca          Chat
         │             │             │
         ▼             ▼             ▼
    Gemma 3 1B   EmbeddingGemma  Gemma 3 1B
                       │
                       ▼
                     NumPy
                       │
                       ▼
              Documentos relevantes
```

---

# Escopo do projeto

Este projeto foi desenvolvido como um **MVP**.

A proposta não foi criar uma arquitetura de processamento documental em larga escala, mas demonstrar de maneira simples e compreensível conceitos relacionados a:

* processamento de documentos;
* modelos de linguagem;
* embeddings;
* busca semântica;
* execução local de modelos;
* organização de código Python.

A arquitetura foi mantida propositalmente simples devido à pequena quantidade de documentos e ao tempo disponível para desenvolvimento.

---

# Autor

**Gamaliel Ghelli**

Projeto desenvolvido como estudo de caso para processo seletivo de Estágio em Dados e Inteligência Artificial.
