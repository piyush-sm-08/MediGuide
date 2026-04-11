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
- 🖥️ Streamlit frontend with role-based dashboards

---

## 🛠 Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** Streamlit
- **Database:** MongoDB (local or Atlas)
- **AI / NLP:** LangChain, Ollama, HuggingFace Embeddings
- **Vector Store:** ChromaDB
- **Authentication:** HTTP Basic Auth with bcrypt password hashing
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

# Install server dependencies
pip install -r server/requirements.txt

# Install client dependencies
pip install -r client/requirements.txt

# Configure environment
# Copy server/.env.example to server/.env and update values
# Copy client/.env.example to client/.env and update BASE_URL

# Start the FastAPI server
uvicorn server.main:app --reload --port 8001

# In a separate terminal, start the Streamlit client
streamlit run client/main.py
```

Open API docs:
```bash
http://127.0.0.1:8001/docs
```

Open Streamlit UI:
```bash
http://127.0.0.1:8501
```

---

## Disclaimer

MediGuide is not a medical diagnosis tool.
It is intended for educational and informational purposes only.

**📌 Status**

🚧 Under active development
More features and improvements coming soon.

---

## ⭐ Future Improvements (Planned)

- Role-based access control
- Better document chunking & retrieval
- Multi-user document isolation
- Enhanced medical safety checks
---