# Uploaded Documents Store

This directory stores uploaded PDF files at the repository root.

## Purpose

- Saves PDF uploads from the frontend and backend.
- Acts as the raw file storage location for document processing.

## How it works

- When a file is uploaded through the app, it is saved here.
- The server reads the saved file to build embeddings and summaries.
- Uploaded documents are referenced by `doc_id` in MongoDB.

## Notes

- This folder is not intended to be a production document server.
- You can delete files here to remove raw uploads, but Chroma embeddings may still remain.
