
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# Load environment variables
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR")
UPLOAD_DIR = "./uploaded_docs"

# Make sure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# Initialize or load Chroma vector store
if Path(CHROMA_PERSIST_DIR).exists() and any(Path(CHROMA_PERSIST_DIR).iterdir()):
    # Load existing Chroma database
    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings
    )
else:
    # Create a new Chroma database
    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings
    )
    vectorstore.persist()



def load_vectorstore(uploaded_files,role:str, doc_id:str):
    embedded_model =  HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR)/file.filename

        with open(save_path , 'wb') as f:
            f.write(file.file.read())

        loader = PyPDFLoader(str(save_path))
        documents = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(chunk_size = 500 , chunk_overlap = 100)
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        ids = [f"{doc_id}-{i}" for i in range(len(chunks))]
        metadata = [
            {
                "source" : file.filename,
                "doc_id" : doc_id,
                "role" : role,
                "page" : chunk.metadata.get("page",0)
            }
            for i, chunk in enumerate(chunks)
        ]               
 
        print(f"Embeddings {len(texts)} chunks ..")
        embeddings_vectors = embedded_model.embed_documents(texts)

        print("Uploading to ChromaDB")

        vectors_to_upsert = [
            {
                "id": ids[i],
                "embedding": embeddings[i],
                "metadata": metadata[i]
            }
            for i in range(len(embeddings))
        ]
 
        with tqdm(total=len(vectors_to_upsert), desc="Upserting to ChromaDB") as progress:
            for vector in vectors_to_upsert:
                vectorstore.upsert([vector])
                progress.update(1)

        print(f"Upload complete for {file.filename}")  