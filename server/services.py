"""
Shared services module — single source of truth for embeddings,
vector store, and LLM initialization across the entire server.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Suppress TensorFlow/Keras warnings before any imports
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Suppress INFO and WARNING logs
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # Disable oneDNN optimizations
os.environ["TF_USE_LEGACY_KERAS"] = "1"  # Keras 2 compatibility

# Load environment variables from server/.env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
UPLOAD_DIR = "./uploaded_docs"

if not EMBEDDING_MODEL or not CHROMA_PERSIST_DIR:
    raise RuntimeError("EMBEDDING_MODEL or CHROMA_PERSIST_DIR not set in .env")

if not OLLAMA_MODEL or not OLLAMA_BASE_URL:
    raise RuntimeError("OLLAMA_MODEL or OLLAMA_BASE_URL not set in .env")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ─── Lazy singletons ────────────────────────────────────────────────
_embeddings = None
_vectorstore = None
_llm = None


def get_embeddings():
    """Return a cached HuggingFaceEmbeddings instance."""
    global _embeddings
    if _embeddings is None:
        # Configure TensorFlow to be less verbose
        import logging
        logging.getLogger('tensorflow').setLevel(logging.ERROR)
        logging.getLogger('absl').setLevel(logging.ERROR)

        from langchain_huggingface import HuggingFaceEmbeddings
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings


def get_vectorstore():
    """Return a cached Chroma vectorstore instance."""
    global _vectorstore
    if _vectorstore is None:
        try:
            from langchain_chroma import Chroma
            _vectorstore = Chroma(
                persist_directory=CHROMA_PERSIST_DIR,
                embedding_function=get_embeddings()
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to initialize Chroma vector store: {exc}") from exc
    return _vectorstore


def get_llm():
    """Return a cached OllamaLLM instance."""
    global _llm
    if _llm is None:
        try:
            from langchain_ollama import OllamaLLM
            _llm = OllamaLLM(
                model=OLLAMA_MODEL,
                base_url=OLLAMA_BASE_URL
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to initialize Ollama LLM: {exc}") from exc
    return _llm


def invoke_llm(prompt: str) -> str:
    """Invoke the LLM with a prompt string and return the response."""
    try:
        return get_llm().invoke(prompt)
    except Exception as exc:
        raise RuntimeError(f"LLM invocation failed: {exc}") from exc
