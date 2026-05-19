# 📚 CompanionBuddy — AI Study Companion

> Upload your notes. Let AI do the heavy lifting.

**Live Demo → [companionbuddy.streamlit.app](https://companionbuddy.streamlit.app)**

---

## What It Does

CompanionBuddy is a RAG-powered study assistant that turns any PDF into an interactive learning session. Upload your lecture notes or textbook chapters and get:

- **Chat** — Ask questions and get answers grounded in *your* document
- **Summaries** — Structured key topics, core concepts, and takeaways
- **Quizzes** — Auto-generated multiple-choice questions with explanations
- **Flashcards** — Term ↔ definition cards for active recall
- **Progress Tracking** — Score history and improvement over time

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM | Groq (llama-3.1-8b-instant) / Gemini 1.5 Flash |
| Embeddings | Jina AI (`jina-embeddings-v2-base-en`) |
| Vector Store | ChromaDB |
| PDF Processing | LangChain + PyPDF |
| Deployment | Streamlit Community Cloud + Render |

---

## Architecture

```
User uploads PDF
      ↓
FastAPI backend
      ↓
PyPDF → LangChain text splitter (chunks of 1500 chars, 100 overlap)
      ↓
Jina embeddings → ChromaDB (persisted vector store)
      ↓
On query: similarity search → top-k chunks → Groq LLM → response
```

---

## Local Setup

### Prerequisites
- Python 3.11
- API keys: [Groq](https://console.groq.com), [Jina AI](https://jina.ai), optionally [Google AI](https://aistudio.google.com)

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GROQ_API_KEY=your_groq_key
JINA_API_KEY=your_jina_key
GOOGLE_API_KEY=your_google_key   # optional
LLM_PROVIDER=groq
EOF

uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Backend runs on `http://localhost:8000`, frontend on `http://localhost:8501`.

---

## Project Structure

```
companion_buddy/
├── frontend/
│   ├── app.py                  # Home page
│   └── pages/
│       ├── 1_Upload.py         # PDF upload & indexing
│       ├── 2_Chat.py           # RAG-powered Q&A
│       ├── 3_Generate.py       # Quiz, summary, flashcards
│       └── 4_Progress.py       # Score history dashboard
├── backend/
│   └── app/
│       ├── main.py             # FastAPI app + CORS
│       ├── config.py           # Settings via pydantic-settings
│       ├── api/                # Route handlers
│       ├── rag/                # Document processor, embeddings, vector store
│       ├── services/           # LLM, chat, generate logic
│       └── prompts/            # LangChain prompt templates
└── packages.txt                # System deps for Streamlit Cloud
```

---

## Deployment

### Frontend — Streamlit Community Cloud
1. Push to GitHub
2. Connect repo at [share.streamlit.io](https://share.streamlit.io)
3. Set main file: `frontend/app.py`
4. No secrets needed (backend URL is hardcoded)

### Backend — Render
1. Create a new **Web Service** pointing to the `backend/` directory
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
4. Add environment variables in the Render dashboard:

```
GROQ_API_KEY=...
JINA_API_KEY=...
GOOGLE_API_KEY=...
LLM_PROVIDER=groq
```

> ⚠️ Render's free tier spins down after inactivity — first request may take ~30s.

---

## Configuration

All settings live in `backend/app/config.py` and can be overridden via environment variables:

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `groq` | `groq` or `gemini` |
| `GROQ_MODEL` | `llama-3.1-8b-instant` | Groq model name |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Gemini model name |
| `CHUNK_SIZE` | `1500` | Characters per chunk |
| `CHUNK_OVERLAP` | `100` | Overlap between chunks |
| `RETRIEVAL_K` | `4` | Chunks retrieved per query |

---

## Known Limitations

- PDF only (no images, scanned docs, or handwriting)
- Uploaded files and ChromaDB are ephemeral on Render's free tier (reset on redeploy)
- First upload may be slow due to Jina API rate limits (batched at 2 chunks/request)

---
