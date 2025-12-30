# 🩺 MediGuide – AI Medical Assistant (MVP)

**MediGuide** is an AI-powered medical assistant built using **FastAPI**, **MongoDB**, and **LangChain**.  
It enables users to interact with medical documents and information through a clean and intuitive API interface.

This project is an **early-stage MVP** and will be continuously enhanced with new features and improvements.

---

## 🚀 Features

- 🔐 User authentication (Signup & Login)
- 📄 Medical document upload (PDF support)
- 🤖 AI-powered question answering using embeddings
- 🔎 Semantic vector search with ChromaDB
- 🗄️ MongoDB for user and application data
- ⚡ FastAPI backend with automatic API documentation

---

## 🛠 Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** MongoDB Atlas
- **AI / NLP:** LangChain, HuggingFace Embeddings
- **Vector Store:** ChromaDB
- **Authentication:** JWT-based Auth
- **Server:** Uvicorn   

---

## ▶️ Run Locally

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload

```
Open:
```bash
http://127.0.0.1:8000/docs
```

## Disclaimer

MediGuide is not a medical diagnosis tool.
It is intended for educational and informational purposes only.

📌 Status

🚧 Under active development
More features and improvements coming soon.

⭐ Future Improvements (Planned)

- Role-based access control
- Better document chunking & retrieval
- Multi-user document isolation
- UI dashboard (Frontend)
- Enhanced medical safety checks