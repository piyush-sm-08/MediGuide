# Server Documents Module

This directory handles document upload, PDF processing, summarization, and metadata storage.

## Files

- `routes.py` – document and report endpoints
- `vector.py` – document parsing, chunking, embedding, and summarization utilities

## Endpoints

- `POST /docs` – upload role-specific reference PDFs (admin only)
- `POST /docs/report` – upload a patient medical report and generate a summary
- `GET /docs/reports` – list accessible saved reports
- `GET /docs/reports/{doc_id}` – retrieve a single saved report

## How it works

1. Uploaded file bytes are saved into `uploaded_docs/`.
2. The server parses the PDF and splits it into text chunks.
3. Each chunk is embedded using the configured HuggingFace model.
4. The vectors are stored in ChromaDB with metadata including source, role, and doc_id.
5. Patient report uploads are also summarized using the Ollama LLM.
6. Report metadata is saved in MongoDB under the `reports` collection.

## Notes

- Admin users upload reference documents for doctors, nurses, patients, or others.
- Patients can upload their own reports and receive a summary.
- Document vectors are filtered by role during chat search.
