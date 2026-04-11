# Server Chat Module

This directory implements question answering via the `/chat` endpoint.

## Files

- `routes.py` – defines the `/chat` POST endpoint
- `chat_query.py` – performs vector similarity search and LLM invocation

## How it works

1. The authenticated user sends a query and `top_k` parameter.
2. `chat_query.answer_query()` performs a filtered similarity search in ChromaDB using the user role.
3. Retrieved documents are assembled into a context prompt.
4. The prompt is sent to the configured Ollama LLM.
5. The server returns an answer and source metadata.

## Notes

- The chat endpoint is role-aware and only returns documents matching the user role.
- If no documents are found, the endpoint returns a friendly fallback message.
