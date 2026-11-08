
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import RetrievalQA

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------
PDF_NAME = "fragmentos-TCC-2016.pdf"          # coloque seu PDF na pasta 'data' e ajuste o nome aqui
PDF_PATH = os.path.join("data", PDF_NAME)

EMBEDDING_MODEL = "mxbai-embed-large"
LLM_MODEL = "llama3.2:latest"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 50
TOP_K = 5                            # quantidade de chunks recuperados por pergunta


def carregar_e_dividir_pdf(pdf_path):
    """Carrega o PDF e divide o texto em chunks."""
    print("📖 Carregando e dividindo o arquivo PDF...")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    texts = text_splitter.split_documents(pages)
    print(f"✅ Texto dividido com sucesso em {len(texts)} chunks.")
    return texts


def criar_banco_vetorial(texts):
    """Gera os embeddings de cada chunk e os insere em um banco FAISS."""
    print("🧠 Gerando embeddings e criando o banco FAISS (pode demorar um pouco)...")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    db = FAISS.from_documents(texts, embeddings)
    print("✅ Banco de dados vetorial FAISS pronto!")
    return db


def criar_cadeia_qa(db):
    """Cria a cadeia RetrievalQA ligada ao banco vetorial."""
    print(f"🤖 Inicializando o modelo {LLM_MODEL}...")
    model = OllamaLLM(model=LLM_MODEL)
    retriever = db.as_retriever(search_kwargs={"k": TOP_K})

    # A cadeia converte a pergunta em embedding, busca os chunks mais próximos
    # no FAISS e envia tudo ao LLM para gerar a resposta final.
    return RetrievalQA.from_chain_type(
        llm=model,
        retriever=retriever,
        chain_type="stuff",
    )


def main():
    if not os.path.exists(PDF_PATH):
        print(f"❌ Erro: coloque o arquivo '{PDF_NAME}' dentro da pasta 'data' antes de rodar.")
        return

    texts = carregar_e_dividir_pdf(PDF_PATH)
    db = criar_banco_vetorial(texts)
    qa_chain = criar_cadeia_qa(db)

    # Loop de perguntas interativas no terminal
    print("\n🚀 Sistema pronto! Digite sua pergunta sobre o documento (ou 'sair' para encerrar):")
    while True:
        query = input("\n👤 Sua pergunta: ")
        if query.lower().strip() in ["sair", "exit", "quit"]:
            print("Encerrando o sistema. Até logo!")
            break

        if not query.strip():
            continue

        print("🔍 Buscando no banco vetorial e gerando resposta...")
        response = qa_chain.invoke(query)
        print(f"🤖 Resposta da IA: {response['result']}")


if __name__ == "__main__":
    main()
