# Server ChromaDB Persistence

This directory holds ChromaDB persistence data when the server is run from the `server/` working directory.

## Purpose

- Stores vector embeddings created from uploaded documents.
- Contains a Chroma SQLite database used by the backend search engine.

## How it is used

- `server/services.py` initializes Chroma using `CHROMA_PERSIST_DIR` from `server/.env`.
- `server/docs/vector.py` adds text embeddings to Chroma.
- `server/chat/chat_query.py` performs similarity search against this store.

## Note

- The Chroma store is the central vector index for document search.
- Do not remove this directory if you want to preserve uploaded document embeddings.
