# Sistema de Perguntas e Respostas com FAISS e RetrievalQA

Este projeto foi feito objetivando praticar o conteudo da Unidade 5 da disciplina Tópicos Específicos em Sistemas para Internet I. A ideia era montar um sistema que responde perguntas sobre um documento usando **embeddings**, um **banco de dados vetorial (FAISS)** e o módulo **RetrievalQA** do LangChain.

Eu usei como base o notebook que o professor deixou no GitHub ([VectorDB com FAISS](https://github.com/tmedeirosb/tsi-llm/blob/main/vb-faiss-un04.ipynb)) e adaptei para um script Python que roda no terminal.

## O que o projeto faz

Eu coloco um PDF na pasta `data/` e o programa:

1. Lê o PDF e divide o texto em pedaços pequenos (chunks) de 1000 caracteres, com 50 de sobreposição.
2. Transforma cada chunk em um vetor (embedding) usando o modelo `mxbai-embed-large` do Ollama.
3. Guarda esses vetores em um banco vetorial FAISS.
4. Quando eu faço uma pergunta, o `RetrievalQA` converte a pergunta em embedding, busca os 5 chunks mais parecidos no FAISS e manda esse conteúdo para o modelo `llama3.2`, que escreve a resposta.

Tudo roda localmente, sem precisar de chave de API.

## Estrutura do repositório

```
.
├── app.py              # código principal
├── requirements.txt    # dependências
├── README.md
├── .gitignore
└── data/
    └── fragmentos-TCC-2016.pdf   # PDF usado nos testes
```

## Como executar

### 1. Pré-requisitos

- Python 3.10 ou superior
- [Ollama](https://ollama.com) instalado

Depois de instalar o Ollama, baixe os dois modelos que eu usei:

```bash
ollama pull mxbai-embed-large
ollama pull llama3.2
```

### 2. Clonar o repositório e criar o ambiente virtual

```bash
git clone https://github.com/everaldoferreira/rag-faiss-retrievalqa.git
cd rag-faiss-retrievalqa
python -m venv venv
source venv/bin/activate      # no Windows: venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Conferir o PDF

O PDF precisa estar em `data/` com o mesmo nome que está na variável `PDF_NAME` do `app.py` (no meu caso, `fragmentos-TCC-2016.pdf`). Se quiser usar outro PDF, é só colocar na pasta `data/` e trocar esse nome no código.

### 5. Rodar

Deixe o Ollama aberto e execute:

```bash
python app.py
```

Primeiro o programa carrega o PDF e cria o banco FAISS (isso pode demorar um pouco). Quando aparecer "Sistema pronto!", é só digitar a pergunta. Para sair, digite `sair`.

## Exemplos de perguntas e respostas

> Estes são testes que eu fiz rodando o programa.

**Pergunta 1:** *Qual átomo é usado na simulação melaço óptico?*

**Resposta:** *Césio*

---

**Pergunta 2:** *Um átomo com um feixe de radiação eletromagnética modifica o que?*

**Resposta:** *Um átomo com um feixe de radiação eletromagnética modifica a velocidade do átomo*

---

**Pergunta 3:** *Que tipo de força precisamos obter para resfriar-mos átomos?*

**Resposta:** *A resposta é uma força de tipo viscosa, proporcional e contrária à velocidade do átomo, de acordo com o ponto de vista defendido por Hänsch e Schawlow.*

## Tecnologias usadas

- Python
- LangChain (`langchain`, `langchain-classic`, `langchain-community`, `langchain-ollama`, `langchain-text-splitters`)
- FAISS (`faiss-cpu`)
- Ollama (`mxbai-embed-large` para embeddings e `llama3.2` para gerar as respostas)
- PyPDF para ler o PDF

## Observações

- Nas versões mais novas do LangChain o `RetrievalQA` foi movido para o pacote `langchain-classic`, por isso o import no meu código é `from langchain_classic.chains import RetrievalQA`.
- Se o modelo não achar a resposta no documento, ele pode responder algo errado ou genérico. A qualidade depende bastante do PDF e de como a pergunta é feita.
- O banco FAISS é criado de novo toda vez que o programa roda, então no começo demora um pouco.

