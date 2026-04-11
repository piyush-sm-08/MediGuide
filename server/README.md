# Server / FastAPI Backend

This folder contains the backend API for MediGuide.

## What it does

- Hosts FastAPI application in `server/main.py`
- Registers authentication, document, and chat routers
- Handles PDF uploads, summary generation, vector storage, and chat responses
- Connects to MongoDB and ChromaDB

## Key components

- `server/main.py` – application entry point
- `server/auth/routes.py` – signup/login and authentication logic
- `server/docs/routes.py` – document upload and retrieval endpoints
- `server/chat/routes.py` – chat query endpoint
- `server/config/db.py` – MongoDB connection and fallback mock database
- `server/services.py` – embeddings, ChromaDB, and LLM singleton initialization

## Environment

The server loads `server/.env` for:

- `MONGODB_URI`
- `MONGODB_DB_NAME`
- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`
- `EMBEDDING_MODEL`
- `CHROMA_PERSIST_DIR`

## Run locally

```bash
pip install -r server/requirements.txt
uvicorn server.main:app --reload --port 8001
```

## Connection overview

- The client communicates with this backend using REST calls.
- The backend uses HTTP Basic auth for login and protected endpoints.
- Document uploads are saved in `uploaded_docs/`.
- Vector embeddings are stored in ChromaDB using the configured `CHROMA_PERSIST_DIR`.
- Chat queries run a similarity search filtered by user role.

## Notes

- If MongoDB is unavailable, the server falls back to an in-memory mock database for development.
- Verify that the client `BASE_URL` points to the same URL and port used for the backend.
