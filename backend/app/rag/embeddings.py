from langchain_community.embeddings import JinaEmbeddings
from app.config import settings
import os

_embedding_model = None

def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        if not settings.jina_api_key:
            raise ValueError("JINA_API_KEY not set in .env")
        
        # Set environment variable so Jina can see it
        os.environ["JINA_API_KEY"] = settings.jina_api_key
        
        print("Loading Jina embeddings...")
        _embedding_model = JinaEmbeddings(
            model_name="jina-embeddings-v2-base-en",
            jina_api_key=settings.jina_api_key  # ← Pass directly
        )
        print("✅ Jina embeddings ready")

    return _embedding_model