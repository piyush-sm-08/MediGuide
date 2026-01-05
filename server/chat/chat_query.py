import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM

load_dotenv()

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

if not all([CHROMA_PERSIST_DIR, EMBEDDING_MODEL, OLLAMA_MODEL]):
    raise RuntimeError("Missing required environment variables")

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

# Vector DB
vectorstore = Chroma(
    persist_directory=CHROMA_PERSIST_DIR,
    embedding_function=embeddings
)

# LLM
llm = OllamaLLM(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL
)


def answer_query(query: str, top_k: int, role: str):
    """
    Core RAG logic (framework independent)
    """

    docs = vectorstore.similarity_search(
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

    answer = llm.invoke(prompt)

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
