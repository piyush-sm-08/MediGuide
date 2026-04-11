# 🩺 MediGuide – AI Medical Assistant (MVP)

**MediGuide** is an AI-based medical assistant built with **FastAPI**, **Streamlit**, **MongoDB**, and **LangChain**. It connects a lightweight web UI to an API backend that stores user data, uploads medical documents, creates semantic embeddings, and answers user questions using vector search.

---

## 📂 Project Structure

- `/client` – Streamlit frontend that handles user authentication, uploads, and chat.
- `/server` – FastAPI backend with authentication, document upload, vectorization, and chat endpoints.
- `/server/auth` – Authentication routes and login/signup logic.
- `/server/docs` – PDF upload, summarization, and metadata storage.
- `/server/chat` – Question answering endpoint and RAG query logic.
- `/server/config` – MongoDB configuration and database connection.
- `/server/chroma_db` and `/chroma_db` – ChromaDB persistence stores for embeddings.
- `/uploaded_docs` and `/server/uploaded_docs` – Saved uploaded PDF files.

---

## 🔌 How It Works

1. The **Streamlit client** reads `BASE_URL` from the root `.env` file and sends HTTP requests to the FastAPI server.
2. The server exposes three main areas:
   - `/signup` and `/login` for user authentication.
   - `/docs` for document upload, report summary, and listing saved documents.
   - `/chat` for role-based medical question answering.
3. Each upload is saved in `uploaded_docs/` and then processed by the server:
   - PDFs are parsed, split into text chunks, and embedded with HuggingFace embeddings.
   - The vectors are persisted into ChromaDB.
   - Medical reports are also summarized through an Ollama LLM.
4. Authenticated users can query the chat endpoint, which performs a similarity search over role-specific document vectors and returns an answer with sources.

---

## ⚙️ Environment Setup

### Server environment (`server/.env`)

This file is required by the FastAPI backend and includes:

- `MONGODB_URI` – MongoDB connection URI (local or Atlas)
- `MONGODB_DB_NAME` – Database name
- `OLLAMA_BASE_URL` – Ollama server URL
- `OLLAMA_MODEL` – Ollama model name
- `EMBEDDING_MODEL` – HuggingFace embedding model
- `CHROMA_PERSIST_DIR` – Chroma persistence directory

Example values are already present in `server/.env` in this workspace.

### Client environment (`.env`)

The Streamlit client uses the root `.env` file and requires:

- `BASE_URL` – URL of the running FastAPI server

Example:

```env
BASE_URL=http://127.0.0.1:8001
```

> If you run the server on port `8001`, make sure `BASE_URL` matches that port.

---

## ▶️ Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r server/requirements.txt
pip install -r client/requirements.txt
uvicorn server.main:app --reload --port 8001
streamlit run client/main.py
```

Then open:

- FastAPI docs: `http://127.0.0.1:8001/docs`
- Streamlit app: `http://127.0.0.1:8501`

---

## 🔗 Connection Flow

- The **client** uses `requests` with HTTP Basic auth to communicate with the FastAPI server.
- The **server** verifies credentials via `server/auth/routes.py`.
- Uploaded documents are stored in `uploaded_docs/` and indexed with Chroma in `chroma_db/`.
- Chat questions are answered by searching the vector store and invoking an LLM.
- MongoDB stores users, report metadata, and role access information.

---

## 📌 Important Notes

- The client expects `BASE_URL` to point to the running FastAPI server.
- The server expects `server/.env` to contain valid model, Chroma, and MongoDB settings.
- `server/config/db.py` will fall back to a mock database if MongoDB is unavailable.

---

## 🗂 README Files in Each Folder

This workspace now includes README documentation in these directories:

- `/client`
- `/server`
- `/server/auth`
- `/server/chat`
- `/server/config`
- `/server/docs`
- `/server/chroma_db`
- `/server/uploaded_docs`
- `/chroma_db`
- `/uploaded_docs`

Each README explains the folder responsibility and how it connects to the rest of MediGuide.
---