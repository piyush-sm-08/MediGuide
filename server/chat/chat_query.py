import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from server/.env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

if not all([CHROMA_PERSIST_DIR, EMBEDDING_MODEL, OLLAMA_MODEL, OLLAMA_BASE_URL]):
    raise RuntimeError("Missing required environment variables")

# Lazy initialization
embeddings = None
vectorstore = None
llm = None

def get_embeddings():
    global embeddings
    if embeddings is None:
        from langchain_huggingface import HuggingFaceEmbeddings
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return embeddings

def get_vectorstore():
    global vectorstore
    if vectorstore is None:
        from langchain_chroma import Chroma
        vectorstore = Chroma(
            persist_directory=CHROMA_PERSIST_DIR,
            embedding_function=get_embeddings()
        )
    return vectorstore

def get_llm():
    global llm
    if llm is None:
        from langchain_ollama import OllamaLLM
        llm = OllamaLLM(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL
        )
    return llm


def answer_query(query: str, top_k: int, role: str):
    """
    Core RAG logic (framework independent)
    """

    docs = get_vectorstore().similarity_search(
        query=query,
        k=top_k,
        filter={"role": role}
    )

    if not docs:
        return {
            "answer": "No relevant medical documents found.",
            "sources": []
        }

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are a medical assistant.

Answer strictly using the context below.
If the answer is not present, say:
"I don't have enough medical information to answer this."

Context:
{context}

Question:
{query}
"""

    answer = get_llm().invoke(prompt)

    return {
        "answer": answer,
        "sources": [
            {
                "source": d.metadata.get("source"),
                "page": d.metadata.get("page"),
                "doc_id": d.metadata.get("doc_id")
            }
            for d in docs
        ]
    }
