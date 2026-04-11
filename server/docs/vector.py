"""
Document vectorization and PDF summarization utilities.
Uses shared services for embeddings, vectorstore, and LLM access.
"""

from pathlib import Path

from ..services import (
    get_vectorstore,
    invoke_llm,
    UPLOAD_DIR,
)


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

        print(f"Upload complete for {filename}")
    except Exception as exc:
        raise RuntimeError(f"Failed to save document vectors: {exc}") from exc


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