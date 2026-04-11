# Root ChromaDB Store

This directory contains the ChromaDB persistence store used when the backend is run from the repository root.

## Purpose

- Holds vector embeddings for document search.
- Contains `chroma.sqlite3` and supporting Chroma store data.

## Connection

- The server configuration uses `CHROMA_PERSIST_DIR` and may resolve to this folder.
- This folder is used by the document upload and chat search pipeline.

## Notes

- Keep this folder if you want to retain embeddings between server restarts.
- Deleting it will remove the vector index and force re-indexing of uploaded documents.
