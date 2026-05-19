import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Force load .env from backend directory
env_path = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    
    llm_provider: str = "groq"
    google_api_key: str = ""
    groq_api_key: str = ""
    jina_api_key: str = ""

    gemini_model: str = "gemini-1.5-flash"
    groq_model: str = "llama-3.1-8b-instant"
    
    upload_dir: str = "uploads"
    chroma_dir: str = "chroma_db"

    chunk_size: int = 1500
    chunk_overlap: int = 100
    retrieval_k: int = 4  

    class Config:
        env_file = str(env_path)  # ← Explicit path


settings = Settings()