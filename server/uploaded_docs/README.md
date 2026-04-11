# Server Uploaded Documents

This directory contains uploaded PDF files when the backend processes documents.

## Purpose

- Saves raw uploaded files from `/docs` and `/docs/report` endpoints.
- Preserves original medical documents for later reference.

## How it is used

- Files are saved with a generated `doc_id` prefix.
- The saved PDFs are then parsed and vectorized by the server.
- Uploaded files are not served directly by default.

## Notes

- It is safe to clean this directory if you want to remove raw uploads, but document vectors may remain in ChromaDB.
