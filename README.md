🩺 MediGuide – Medical Assistant (MVP)

MediGuide is a simple AI-powered medical assistant built using FastAPI, MongoDB, and LangChain.
It helps users interact with medical information and documents through a clean API interface.

This is an early-stage MVP and will be improved with more features over time.

🚀 Features

User authentication (signup & login)

Medical document upload (PDFs)

AI-powered question answering using embeddings

Vector search using ChromaDB

MongoDB for user and application data

FastAPI backend with automatic API docs

🛠 Tech Stack

Backend: FastAPI (Python)

Database: MongoDB Atlas

AI / NLP: LangChain, HuggingFace embeddings

Vector Store: ChromaDB

Auth: JWT-based authentication

Server: Uvicorn

▶️ Run Locally

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --reload
```
Open:
```bash
http://127.0.0.1:8000/docs
```

⚠️ Disclaimer

MediGuide is not a medical diagnosis tool.
It is intended for educational and informational purposes only.

📌 Status

🚧 Under active development
More features and improvements coming soon.