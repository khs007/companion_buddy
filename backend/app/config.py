# File: backend/app/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    llm_provider: str = "groq"

    google_api_key: str = ""
    groq_api_key: str = ""

    gemini_model: str = "gemini-1.5-flash"
    groq_model: str = "llama-3.1-8b-instant"    

    # Embedding model (runs locally, no API key needed)
    embedding_model: str = "all-MiniLM-L6-v2"

    # Storage paths
    upload_dir: str = "uploads"
    chroma_dir: str = "chroma_db"

    # RAG settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_k: int = 4  

    class Config:
        env_file = ".env"


# Single instance used across the whole app
settings = Settings()