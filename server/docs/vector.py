import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
UPLOAD_DIR = "./uploaded_docs"

if not EMBEDDING_MODEL or not CHROMA_PERSIST_DIR:
    raise RuntimeError("EMBEDDING_MODEL or CHROMA_PERSIST_DIR not set")

if not OLLAMA_MODEL or not OLLAMA_BASE_URL:
    raise RuntimeError("OLLAMA_MODEL or OLLAMA_BASE_URL not set")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Lazy initialization of embeddings and vectorstore
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
        try:
            from langchain_chroma import Chroma
            vectorstore = Chroma(
                persist_directory=CHROMA_PERSIST_DIR,
                embedding_function=get_embeddings()
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to initialize Chroma vector store: {exc}") from exc
    return vectorstore

def get_llm():
    global llm
    if llm is None:
        try:
            from langchain_ollama import OllamaLLM
            llm = OllamaLLM(
                model=OLLAMA_MODEL,
                base_url=OLLAMA_BASE_URL
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to initialize Ollama LLM: {exc}") from exc
    return llm


def save_upload_file(uploaded_file) -> Path:
    save_path = Path(UPLOAD_DIR) / uploaded_file.filename
    content = uploaded_file.file.read()
    save_path.write_bytes(content)
    return save_path


def load_vectorstore(file_path: str, filename: str, role: str, doc_id: str):
    """
    Loads a PDF file, splits it into chunks,
    embeds the text, and stores it in ChromaDB.
    """
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from tqdm.auto import tqdm

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    if not chunks:
        return

    texts = [chunk.page_content for chunk in chunks]
    ids = [f"{doc_id}-{i}" for i in range(len(chunks))]
    metadatas = [
        {
            "source": filename,
            "doc_id": doc_id,
            "role": role,
            "page": chunk.metadata.get("page", 0)
        }
        for chunk in chunks
    ]

    print(f"Processing {filename}")
    print(f"Total chunks: {len(texts)}")

    try:
        with tqdm(total=len(texts), desc="Uploading to ChromaDB") as progress:
            get_vectorstore().add_texts(
                texts=texts,
                metadatas=metadatas,
                ids=ids
            )
            progress.update(len(texts))

        get_vectorstore().persist()
        print(f"Upload complete for {filename}")
    except Exception as exc:
        raise RuntimeError(f"Failed to save document vectors: {exc}") from exc


def invoke_llm(prompt: str) -> str:
    try:
        return get_llm().invoke(prompt)
    except Exception as exc:
        raise RuntimeError(f"LLM invocation failed: {exc}") from exc


def summarize_pdf(file_path: str) -> str:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
    except Exception as exc:
        return f"Unable to read PDF for summary: {exc}"

    if not documents:
        return "No content found in the uploaded PDF."

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    if not chunks:
        return "Unable to extract text from the uploaded PDF."

    summaries = []
    for index, chunk in enumerate(chunks):
        prompt = f"""
You are a medical report summarization assistant.
Read the following excerpt from a medical report and create a concise summary in plain language.
Do not hallucinate. Preserve the meaning exactly.

Excerpt:
{chunk.page_content}
"""
        try:
            summaries.append(invoke_llm(prompt))
        except RuntimeError as llm_error:
            fallback = chunk.page_content.strip()
            if len(fallback) > 500:
                fallback = fallback[:500] + "..."
            summaries.append(
                f"[AI unavailable] Extracted text fallback:\n{fallback}"
            )

    if len(summaries) == 1:
        return summaries[0]

    joined = "\n\n".join(summaries)
    final_prompt = f"""
You have the following partial summaries of a medical report. Combine them into one clear and concise summary.

Partial summaries:
{joined}
"""

    try:
        return invoke_llm(final_prompt)
    except RuntimeError:
        return joined